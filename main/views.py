from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json, datetime, os, binascii
from main.models import Player, Group, Table, League_Game, Ranking, Player_Confirmation
from main.util import json_response, send_email, json_payload
from main.domain import decide_points, decide_bonus_points, group_players
from django.db.models import Sum
from django.contrib.auth.models import User

def basic_json(value):
    return {'id': value.id, 'name': value.name}

def json_game(game):
    table = basic_json(game.table)
    player = basic_json(game.player)
    return {'id': game.id, 'table': table, 'player': player, 'score': game.score, 'league_points': game.league_points, 'bonus_points': game.bonus_points}

def json_group(group, games):
    tables = [basic_json(table) for table in {game.table for game in games}]
    players = [basic_json(player) for player in {game.player for game in games}]
    return {'group': group, 'tables': tables, 'players': players}

def fetch_players(request):
    players = [basic_json(player) for player in Player.objects.all()]
    return json_response(players)

def fetch_tables(request):
    # def best_game(table):
    #     games = League_Game.objects.filter(table__id=table['id']).order_by('-score')
    #     if len(games) > 0:
    #         high_score = games[0]
    #         return {'player': high_score.player.name, 'score': high_score.score, 'week': high_score.group.week}
    #     else:
    #         return {}
    tables = list(Table.objects.all().values())
    # for table in tables:
    #     table['best_game'] = best_game(table)
    return json_response(tables)

def fetch_group(request):
    group = Group.objects.get(week=request.GET.get('week'), group=request.GET.get('group'))
    gameObjs = group.games.all()
    games = [json_game(game) for game in gameObjs]
    tables = [{'id': table.id, 'name': table.name} for table in {game.table for game in gameObjs}]
    return json_response({'group': group.group, 'week': group.week, 'games': games, 'tables': tables})

def overview(request):
    rankings = [ranking.week for ranking in Ranking.objects.all()]
    week = max(rankings) if rankings else 1
    rankings = []
    for rank in Ranking.objects.filter(week=week):
        rankings.append({'rank': rank.rank, 'player': player_name(rank.player), 'points': rank.points, 'week': rank.week})
    return json_response({'rankings': rankings, 'week':week})

def setup_week(request, week):
    players = League_Game.objects.filter(group__week=int(week)-1).values('group__group', 'player__name', 'player').annotate(points=Sum('league_points', field='league_points+bonus_points'))
    groups = {group+1: [] for group in range(len({player['group__group'] for player in players}))}
    for player in players:
        print player
        # groups[player['group__group']].append({'name': player['player__name'], 'id': player['player'], 'league_points': player['points']})
    model = group_players(groups)
    return json_response(model)

@ensure_csrf_cookie
def save_groups(request):
    if request.method == 'POST':
        payload = json.loads(request.POST.dict().keys()[0])
        week = payload['week']
        for i, g in enumerate(payload['groups']):            
            group = Group()
            group.week = week
            group.group = i+1
            group.save()
            players = [Player.objects.get(id=player['id']) for player in g['players']]
            tables = [Table.objects.get(id=table['id']) for table in g['tables']]
            for (player, table) in [(player, table) for player in players for table in tables ]:
                game = League_Game()
                game.player = player
                game.table = table
                game.group = group
                game.save()
            for player in players:
                ranking = Ranking()
                ranking.player = player
                ranking.week = week
                for p in g['players']:
                    if p['id'] == player.id:
                        ranking.rank = p['rank']
                        total_points = 0
                        for game in League_Game.objects.filter(player=player):
                            points = game.league_points if game.league_points is not None else 0
                            bonus_points = game.bonus_points if game.bonus_points is not None else 0
                            total_points = total_points + (points + bonus_points)
                        ranking.points = total_points
                ranking.save()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)

def user_can_enter_scores(user, group, week):
    player = Player.objects.filter(user=user)
    modelGroup = Group.objects.filter(group=group, week=week)
    games = League_Game.objects.filter(player=player, group=modelGroup)
    return True if games or user.is_superuser else False

from django.contrib.auth.decorators import login_required
@ensure_csrf_cookie 
@login_required
def save_games(request):
    if request.method == 'POST':
        payload = json.loads(request.POST.dict().keys()[0])
        games = payload['games']
        scores = sorted([game['score'] for game in games],reverse=True)
        points = []
        for game in games:
            savedGame = League_Game.objects.get(id=game['id'])
            savedGame.score = game['score']
            savedGame.league_points = decide_points(scores, savedGame.score)
            savedGame.bonus_points = decide_bonus_points(scores, savedGame.score)
            points.append({'id': game['id'], 'league_points': savedGame.league_points, 'bonus_points': savedGame.bonus_points})
            savedGame.save()
        return json_response(points, 201)
    else:
        return HttpResponse(status=400)

from django.views.generic import View

class IndexView(View):
    def get(self, request):
        weeks = [group.week for group in Group.objects.distinct('week')]
        maxWeek = max(weeks) if weeks else 1

        rankings = [ranking.week for ranking in Ranking.objects.all()]
        week = max(rankings) if rankings else 1
        print week
        rankings = Ranking.objects.filter(week=week)
        print rankings
        return render(request, 'index.html', {'weeks': weeks, 'rankings': rankings})

class TableView(View):
    def get(self, request):
        tables = Table.objects.all()
        return render(request, 'tables.html', {'tables': tables})

class PlayerView(View):
    def get(self, request):
        players = Player.objects.all()
        return render(request, 'players.html', {'players': players})

from main.forms import SignupForm
class SignupView(View):
    form_class = SignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            pc = Player_Confirmation()
            pc.username = form.cleaned_data['username']
            pc.email = form.cleaned_data['email']
            pc.confirmation_token = binascii.hexlify(os.urandom(16))
            pc.save()
            if 'USE_LOCAL_DB' not in os.environ:
                send_email(pc.email, pc.confirmation_token) 
            else:
                print pc.confirmation_token
            return render(request, 'signup_accepted.html', {'email': pc.email})
        else:
            return render(request, 'signup.html', {'form': form})

from main.forms import AccountConfirmationForm
class ConfirmAccountView(View):
    form_class = AccountConfirmationForm

    def get(self, request, token):
        pc = Player_Confirmation.objects.get(confirmation_token=token)
        form = self.form_class()
        return render(request, 'confirm_account.html', {'token': token, 'player_confirmation': pc, 'form': form})

    def post(self, request, token):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                pc = Player_Confirmation.objects.get(confirmation_token=token)
            except Player_Confirmation.DoesNotExist:
                return HttpResponse(status=404)

            user = User.objects.create_user(pc.username, pc.email, form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            
            player = Player()
            player.signature = form.cleaned_data['signature']
            player.ifpa_id = form.cleaned_data['ifpa_id']
            player.user = user
            player.save()
            pc.delete()
            return redirect('/login?confirmed=true')
        else:
            pc = Player_Confirmation.objects.get(confirmation_token=token)
            return render(request, 'confirm_account.html', {'token': token, 'player_confirmation': pc, 'form': form})

class SetupWeekView(View):

    def get(self, request):
        from django.db.models import Max
        groups = Group.objects.all().aggregate(Max('week'))   
        week = groups['week__max']+1 if groups['week__max'] else 1
        return render(request, 'setup_week.html', {'week': week})

class WeekView(View):

    def get(self, request, week):
        groups = Group.objects.filter(week=week)
        return render(request, 'week.html', {'week': week, 'groups': groups})

class GroupView(View):

    def get(self, request):
        (week, group) = (request.GET.get('week'), request.GET.get('group'))
        canEnterScores = user_can_enter_scores(request.user, week, group) if request.user.is_authenticated() else False
        return render(request, 'group.html', {'week': week, 'group': group, 'canEnterScores': canEnterScores})

from django.contrib.auth import authenticate, login, logout
class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {'confirmed': request.GET.get('confirmed')})
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'status': 'notActive'})
        else:
            return render(request, 'login.html', {'status': 'failed'})

class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')

