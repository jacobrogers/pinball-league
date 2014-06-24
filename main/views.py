from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from main.models import Player, Group, Table, League_Game, Ranking
from main.util import json_response

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
    return json_response(list(Player.objects.all().values()))

def fetch_tables(request):
    return json_response(list(Table.objects.all().values()))

def fetch_groups(request, week):
    groups = [json_group(group.group, group.games.all()) for group in Group.objects.filter(week=week)]
    return json_response({'week': week, 'groups': groups})

def fetch_group(request):
    group = Group.objects.get(week=request.GET.get('week'), group=request.GET.get('group'))
    gameObjs = group.games.all()
    games = [json_game(game) for game in gameObjs]
    tables = [{'id': table.id, 'name': table.name} for table in {game.table for game in gameObjs}]
    return json_response({'group': group.group, 'week': group.week, 'games': games, 'tables': tables})

def overview(request):
    from django.db.models import F, Max
    week = 0
    rankings = []
    for rank in Ranking.objects.annotate(max_week=Max('week')).filter(week=F('max_week')):
        week = rank.week
        rankings.append({'rank': rank.rank, 'player': rank.player.name, 'points': rank.points})
    
    return json_response({'rankings': rankings, 'week':week})

def index(request):
    weeks = [group.week for group in Group.objects.distinct('week')]
    nextWeek = 1 if len(weeks) == 0 else max(weeks)+1
    return render(request, 'base.html', {'weeks': weeks, 'nextWeek': nextWeek})

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
                ranking.save()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)

def decide_points(scores, score):
    if score == scores[0]:
        return 3
    if score == scores[-1]:
        return 0
    if score == scores[1]:
        return 2
    return 1

def decide_bonus_points(scores, score):
    if len(scores) == 2:
        if score == scores[0]:
            return 1 if score > scores[1]*3 else 0
        if score == scores[1]:
            return 0 if scores[0] > scores[1]*3 else 1
    else:
        if score == scores[0]:
            return 1 if score > scores[1]+scores[2] else 0
        if len(scores) == 3:
            if score == scores[2]:
                return 0 if scores[0] > scores[1]+scores[2] else 1
        if len(scores) == 4:
            if score == scores[1]:
                return 1 if score > scores[2]+scores[3] else 0
            if score == scores[2]:
                return 0 if scores[0] > scores[1]+scores[2] else 1
            if score == scores[3]:
                return 0 if scores[1] > scores[2]+scores[3] else 1
        return 0

@ensure_csrf_cookie
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