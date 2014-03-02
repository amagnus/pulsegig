from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from app.models import Band, Alert, Guy, AlertLog
from app import songkick
from app import toolbox


''' for each band from DB:
    retrieve users who have alert for this band
        if there shows in user's location for this band:
            if this is a new show (check eventID against AlertLog for user):
                text(user, band, date, url)
                add entry to AlertLog

    changes:
        - edit text output to add proper entry to AlertLog
        - set is_similar=1 if it's a similar band
        - include pulling of similar bands
	    - check what similar bands exist for input band
	    - create array of similar bands after checking for alert on one band
'''


class Command(BaseCommand):

    def handle(self, *args, **options):

        allbands = Band.objects.all()

        for x in allbands:
	    userselect = Alert.objects.filter(band=x, disabled=0).values('user')

	    for y in userselect:
		userone = Guy.objects.filter(user=y['user']).values('metroareaID', 'user')
		bandone = Band.objects.filter(skID=x.skID).values('skID', 'name')

	        show_found = songkick.event_search(bandone[0]['skID'], userone[0]['metroareaID'])

		if len(show_found) != 0:
		    existing = AlertLog.objects.filter(user=y['user'], eventskID=show_found['eventskID']).values('showDate')

		    if len(existing) == 0:
		        new_alertlog = AlertLog(user=User.objects.get(pk=y['user']),
								band=x,
								eventskID=show_found['eventskID'],
								showDate=show_found['date'],
								showURL=show_found['eventURL'],
								send_on=toolbox.gen_send_date(userone[0]['user'], 1))
			new_alertlog.save()


