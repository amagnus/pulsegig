from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from app.models import Guy, AlertLog
from app import toolbox
from app import sendtwilio
import datetime


''' for alertlogs with has_sent=0:
        - if send_on is past current date
            - send text alert to user
            - set has_sent=1 '''


class Command(BaseCommand):

    def handle(self, *args, **options):

        all_alertlogs = AlertLog.objects.filter(has_sent=0)

        for x in all_alertlogs:
            if x.send_on < datetime.datetime.now():
                single_user = Guy.objects.get(pk=x.user)

                if x.is_similar == 1:
                    sendtwilio.send_text(single_user.cell, 'New Suggested Show for ' + x.band.name + ' on ' + str(x.showDate) + ' ' + toolbox.googl_shorten_url(x.showURL))
                else:
                    sendtwilio.send_text(single_user.cell, 'New Show for ' + x.band.name + ' on ' + str(x.showDate) + ' ' + toolbox.googl_shorten_url(x.showURL))

                x.has_sent = 1
                x.save()

