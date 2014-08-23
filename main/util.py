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

def json_response(results, status=200):
    return HttpResponse(to_json(results), status=status, content_type="application/json")

def send_email(email, token):
    import os
    import smtplib

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart('alternative')

    msg['Subject'] = "Confirmation required."
    msg['From']    = "Como Pinball League <como.pinball.league@gmail.com>" # Your from name and email address
    msg['To']      = email

    text = "Mandrill speaks plaintext"
    part1 = MIMEText(text, 'plain')

    html = '<a href="http://como-pinball-league.herokuapp.com/confirmAccount?t=%s">Confirm Account</a>' % tokenw
    part2 = MIMEText(html, 'html')

    username = os.environ['MANDRILL_USERNAME']
    password = os.environ['MANDRILL_APIKEY']

    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('smtp.mandrillapp.com', 587)

    s.login(username, password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())

    s.quit()
    return HttpResponse(status=200)