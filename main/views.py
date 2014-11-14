from main.models import Player, Group, Table, Ranking
from main.util import json_response

def basic_json(value):
    return {'id': value.id, 'name': value.name}

def json_game(game):
    table = basic_json(game.table)
    player = basic_json(game.player)
    player['total_points'] = game.player.total_points
    return {'id': game.id, 'table': table, 'player': player, 'score': game.score, 'league_points': game.league_points, 'bonus_points': game.bonus_points}

def fetch_players(request):
    players = [basic_json(player) for player in Player.objects.all()]
    return json_response(players)

def fetch_tables(request):
    tables = [basic_json(table) for table in Table.objects.filter(status='Active')]
    return json_response(tables)

def fetch_group(request):
    group = Group.objects.get(week=request.GET.get('week'), group=request.GET.get('group'))
    gameObjs = group.games.all()
    games = [json_game(game) for game in gameObjs]
    tables = [{'id': table.id, 'name': table.name} for table in {game.table for game in gameObjs}]
    return json_response({'group': group.group, 'week': group.week, 'games': games, 'tables': tables})