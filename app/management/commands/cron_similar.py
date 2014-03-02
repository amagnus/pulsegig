from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from app.models import Band, Alert, SimilarBand
from app import songkick


''' for each band user entered
		- retrieve similar bands touring now from SK
		- add those to Band model if skID does not exist
		- add entry to SimilarBand if binding does not exist yet / or set disabled=0
		- set disabled=1 to all other existing bindings for input band
        - alter all prod tables to innoDB
        - remove duplicates in initial pool of alerts

	what kind of songkick call are we making
		- similar bands for this band
		- which of the similar bands returned have concerts
		- which of those concerts are happening in location
'''



class Command(BaseCommand):

    def handle(self, *args, **options):

        all_alerts = Alert.objects.filter(disabled=0)

        for x in all_alerts:
            single_band = Band.objects.get(pk=x.band.id)

            get_similar = songkick.search_similar_bands(single_band.skID)

            # make array of all bindings for band_input
            bindings = [ x for x in SimilarBand.objects.filter(band_input=single_band).values_list('band_suggest', flat=True) ]


            for key, value in get_similar.items():
                band_in_db, created = Band.objects.get_or_create(skID=key, defaults={'name': value})

                similar_in_db, created = SimilarBand.objects.get_or_create(band_input=Band.objects.get(pk=single_band.id),
                    band_suggest=band_in_db)

                if created == False and similar_in_db.disabled == 1:
                    similar_in_db.disabled = 0
                    similar_in_db.save()

                if band_in_db.pk in bindings:
                    bindings.remove(band_in_db.pk)


            # set disabled=1 to all other bindings for input band
            for x in bindings:
                bind = SimilarBand.objects.get(band_input=single_band, band_suggest=x)
                bind.disabled = 1
                bind.save()

