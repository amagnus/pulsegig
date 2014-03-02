from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from app.models import Band, Alert, Guy, AlertLog, SimilarBand
from app import songkick
from app import toolbox


''' Changes:
        - set is_similar=1 if it's a similar band
        - include pulling of similar bands
	    	- check what similar bands exist for input band
	    	- create array of similar bands after checking for alert on one band
'''


class Command(BaseCommand):

    def handle(self, *args, **options):

		all_bands = Band.objects.all()

		for x in all_bands:
			all_similar = SimilarBand.objects.filter(band_input=x)

			user_select = Alert.objects.filter(band=x, disabled=0).values_list('user', flat=True)

			for y in user_select:
				single_user = Guy.objects.get(pk=y)

				for z in all_similar:
					single_band = Band.objects.get(pk=z.band_suggest.id)

					show_found = songkick.event_search(single_band.skID, single_user.metroareaID)

					if len(show_found) != 0:
						existing = AlertLog.objects.filter(user=y, eventskID=show_found['eventskID']).values('showDate')

						if len(existing) == 0:
							new_alertlog = AlertLog(user=User.objects.get(pk=y),
													band=single_band,
													eventskID=show_found['eventskID'],
													showDate=show_found['date'],
													showURL=show_found['eventURL'],
													is_similar=1,
													send_on=toolbox.gen_send_date(y))
							new_alertlog.save()

