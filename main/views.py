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
    return json.dumps(list(value), cls=JSONEncoder)

def json_response(results):
    return HttpResponse(to_json(results), content_type="application/json")

def fetch_players(request):
    return json_response(Player.objects.all().values())

def fetch_tables(request):
    return json_response(Table.objects.all().values())

def players_page(request):
    model = {'players': Player.objects.all()}
    return render(request, 'players.html', model)
    
def tables_page(request):
    model = {'tables': Table.objects.all()}
    return render(request, 'tables.html', model)

def create_groups(request):
    return render(request, "create_group.html", {})

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
