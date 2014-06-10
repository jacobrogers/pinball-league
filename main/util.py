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

def to_json(value):
    return json.dumps(value, cls=JSONEncoder)

def json_response(results):
    return HttpResponse(to_json(results), content_type="application/json")