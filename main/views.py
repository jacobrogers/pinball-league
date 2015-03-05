from main.models import Player, Group, Table, Ranking, League_Game
from main.util import json_response

def basic_json(value):
    return {'id': value.id, 'name': value.name}

def json_game(game):
    player = basic_json(game.player)
    return {'id': game.id, 'player': player, 'score': game.score, 'league_points': game.league_points}

def fetch_players(request):
    players = [basic_json(player) for player in Player.objects.all()]
    return json_response(players)

def fetch_tables(request):
    tables = [basic_json(table) for table in Table.objects.filter(status='Active')]
    return json_response(tables)

def fetch_group(request):
    group = Group.objects.get(week=request.GET.get('week'), group=request.GET.get('group'))

    tables = [game.table for game in group.games.distinct('table')]
    matches = []
    for table in tables:
        games = [{'id': game.id, 'player': {'id': game.player.id, 'name': game.player.name}, 'league_points': game.league_points} for game in group.games.filter(table=table)]
        matches.append({'games': games, 'table': {'id': table.id, 'name': table.name}})
    model = {'matches': matches}
    model['tables'] = [basic_json(table) for table in Table.objects.filter(status='Active')]
    model['players'] = [basic_json(player) for player in group.players.all()]
    model['week'] = group.week
    model['group'] = group.group
    # players = []
    # # for player in group.players.all()
        
    # model = {'group': group.group, 'week': group.week}
    return json_response(model)