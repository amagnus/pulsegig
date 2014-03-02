import requests
import json
import datetime
from django.conf import settings
from .models import AlertLog


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if settings.DEBUG == True:
        return settings.DEV_PUBLIC_IP
    else:
        return ip


def googl_shorten_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url'
    payload = {'longUrl': url, 'key': settings.GOOGLE_URL}
    headers = {'content-type': 'application/json'}
    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    raw = json.loads(r.text)
    return raw['id']


''' - if user has 0 alertlog in queue
        - send_on = now
    - if user has 1 alerlogs or more in queue
        - retrieve latest item in queue
        - send_on = next day after latest item's send_on at 11:30am '''

def gen_send_date(userID, now=None):
    queue = AlertLog.objects.filter(has_sent=0, user=userID).count()

    if queue == 0 or now == 1:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        latest = AlertLog.objects.filter(user=userID).order_by('-send_on').values_list('send_on', flat=True)
        send_date = latest[0] + datetime.timedelta(days=1)
        return send_date.strftime('%Y-%m-%d 11:30:00')

