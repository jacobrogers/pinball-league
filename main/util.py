from django.core.serializers.json import DjangoJSONEncoder
import json, datetime
from django.http import HttpResponse

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'): #handles both date and datetime objects
            return obj.isoformat()
        elif isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        else:
            return json.JSONEncoder.default(self, obj)
def basic_json(value):
    return {'id': value.id, 'name': value.name}
    
def to_json(value):
    return json.dumps(value, cls=JSONEncoder)

def json_response(results, status=200):
    return HttpResponse(to_json(results), status=status, content_type="application/json")

def json_payload(request):
    return json.loads(request.POST.dict().keys()[0])