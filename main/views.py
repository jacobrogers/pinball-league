from django.shortcuts import render
from main.models import Player, Group, Table
import json, datetime
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

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

def create_groups(request):
	model = {"players": Player.objects.all()}
	return render(request, "create_group.html", model)
