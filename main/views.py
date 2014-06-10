from django.shortcuts import render
import json, datetime
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import ensure_csrf_cookie

from main.models import Player, Group, Table, League_Game

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'): #handles both date and datetime objects
            return obj.isoformat()
        elif isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        else:
            return json.JSONEncoder.default(self, obj)

def to_json(value):
    return json.dumps(value, cls=JSONEncoder)

def json_response(results):
    return HttpResponse(to_json(results), content_type="application/json")

def fetch_players(request):
    return json_response(list(Player.objects.all().values()))

def fetch_tables(request):
    return json_response(list(Table.objects.all().values()))

def fetch_groups(request, week):
    def create_group(group, games):
        tables = [{'id': table.id, 'name': table.name} for table in {game.table for game in games}]
        players = [{'id': player.id, 'name': player.name} for player in {game.player for game in games}]
        return {'group': group, 'tables': tables, 'players': players}

    groups = [create_group(group.group, group.games.all()) for group in Group.objects.filter(week=week)]
    return json_response({'week': week, 'groups': groups})

def fetch_group(request):
    def create_game(game):
        table = {'id': game.table.id, 'name': game.table.name}
        player = {'id': game.player.id, 'name': game.player.name}
        return {'id': game.id, 'table': table, 'player': player}

    group = request.GET.get('group')
    week = request.GET.get('week')
    games = [create_game(game) for game in Group.objects.get(week=week, group=group).games.all()]
    return json_response({'group': group, 'week': week, 'games': games})

def index(request):
    return render(request, 'base.html', {'homeTab': 'active'})

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
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)
