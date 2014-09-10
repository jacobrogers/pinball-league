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
    players = League_Game.objects.filter(group__week=int(week)-1).values('group__group', 'player').annotate(points=Sum('league_points', field='league_points+bonus_points'))
    groups = {group+1: [] for group in range(len({player['group__group'] for player in players}))}
    for player in players:
        real_player = Player.objects.get(id=player['player'])
        groups[player['group__group']].append({'name': real_player.name, 'id': real_player.id, 'league_points': player['points']})
    def player_has_game(player):
        for p in players:
            if p['player'] == player.id:
                return True
        return False
    new_players = [basic_json(player) for player in Player.objects.all() if not player_has_game(player)]
    model = {'groups': group_players(groups), 'players': new_players}
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
    weeks = [g.week for g in Group.objects.distinct('week')]
    currentWeek = max(weeks)
    player = Player.objects.filter(user=user)
    modelGroup = Group.objects.filter(group=group, week=week)
    games = League_Game.objects.filter(player=player, group=modelGroup)
    return True if (games or user.is_superuser) and currentWeek == int(week) else False

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

def addWeeksToModel(model):
    weeks = [group.week for group in Group.objects.distinct('week')]
    model['weeks'] = weeks
    return model

class BaseView(View):
    template = 'index.html'

    def get(self, request, *args, **kwargs):
        model = self.doGet(request)
        addWeeksToModel(model)
        return render(request, self.template, model)

    def doGet(self, request):
        print 'doGet not overrided'

class IndexView(BaseView):
    template = 'index.html'

    def doGet(self, request):
        weeks = [group.week for group in Group.objects.distinct('week')]
        maxWeek = max(weeks) if weeks else 1

        rankings = [ranking.week for ranking in Ranking.objects.all()]
        week = max(rankings) if rankings else 1
        rankings = Ranking.objects.filter(week=week)
        return {'weeks': weeks, 'rankings': rankings}

class TableView(BaseView):
    template = 'tables.html'

    def doGet(self, request):
        tables = Table.objects.all()
        return {'tables': tables}

class PlayerView(View):

    template = 'player.html'

    def get(self, request, id):
        from operator import itemgetter, attrgetter
        player = Player.objects.get(id=id)
        games = player.games.all()
        player_games = []
        for table in sorted({game.table for game in games}, key=attrgetter('name')):
            game = {'table': {'name': table.name, 'id': table.id} }
            game['scores'] = sorted([{'week': g.group.week, 'score': g.score} for g in games if g.table == table], key=itemgetter('score'), reverse=True)
            player_games.append(game)
        model = {'player': player, 'games': player_games}
        addWeeksToModel(model)
        return render(request, self.template, model)

class PlayersView(BaseView):
    template = 'players.html'

    def doGet(self, request):
        players = Player.objects.all()
        return {'players': players}

from main.forms import SignupForm
class SignupView(BaseView):
    form_class = SignupForm
    template = 'signup.html'

    def doGet(self, request):
        form = self.form_class()
        return {'form': form}

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            pc = Player_Confirmation()
            pc.username = form.cleaned_data['username'].lower()
            pc.email = form.cleaned_data['email'].lower()
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
        model = {'token': token, 'player_confirmation': pc, 'form': form}
        addWeeksToModel(model)
        return render(request, 'confirm_account.html', model)

    def post(self, request, token):
        form = self.form_class(request.POST)

        if form.is_valid():
            try:
                pc = Player_Confirmation.objects.get(confirmation_token=token)
            except Player_Confirmation.DoesNotExist:
                return HttpResponse(status=404)

            user = User.objects.create_user(pc.username, pc.email, form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name'].lower()
            user.last_name = form.cleaned_data['last_name'].lower()
            user.save()
            
            player = Player()
            player.first_name = user.first_name
            player.last_name = user.last_name
            player.signature = form.cleaned_data['signature'].upper()
            player.ifpa_id = form.cleaned_data['ifpa_id']
            player.user = user
            player.save()
            pc.delete()
            return redirect('/login?confirmed=true')
        else:
            pc = Player_Confirmation.objects.get(confirmation_token=token)
            return render(request, 'confirm_account.html', {'token': token, 'player_confirmation': pc, 'form': form})

class SetupWeekView(BaseView):
    template = 'setup_week.html'

    def doGet(self, request):
        from django.db.models import Max
        groups = Group.objects.all().aggregate(Max('week'))   
        week = groups['week__max']+1 if groups['week__max'] else 1
        return {'week': week}

class WeekView(View):

    def get(self, request, week):
        groups = Group.objects.filter(week=week)
        model_groups = []
        for g in groups:
            group = {'tables': [], 'players': [], 'group': g.group}
            for game in g.games.all():
                if game.table not in group['tables']:
                    group['tables'].append(game.table)
                if game.player not in group['players']:
                    group['players'].append(game.player)
                    group['canEnterScores'] = user_can_enter_scores(request.user, week, group['group']) if request.user.is_authenticated() else False
            model_groups.append(group)
        model = {'week': week, 'groups': model_groups}
        addWeeksToModel(model)
        return render(request, 'week.html', model)

class GroupView(BaseView):
    template = 'group.html'

    def doGet(self, request):
        (week, group) = (request.GET.get('week'), request.GET.get('group'))
        canEnterScores = user_can_enter_scores(request.user, week, group) if request.user.is_authenticated() else False
        return {'week': week, 'group': group, 'canEnterScores': canEnterScores}

from django.contrib.auth import authenticate, login, logout
class LoginView(BaseView):
    template = 'login.html'

    def doGet(self, request):
        return {'confirmed': request.GET.get('confirmed')}
    
    def post(self, request):
        username = request.POST['username'].lower()
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

