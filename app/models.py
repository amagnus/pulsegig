from django.db import models
from django.contrib.auth.models import User


class Guy(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    cell = models.CharField(max_length=15)
    metroarea_name = models.CharField(max_length=30, default=None, null=True)
    metroareaID = models.IntegerField(default=None, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user


class Band(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    skID = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class SimilarBand(models.Model):
    band_input = models.ForeignKey(Band, related_name='band_input')
    band_suggest = models.ForeignKey(Band, related_name='band_suggest')
    disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.band_input.name


class Alert(models.Model):
    user = models.ForeignKey(User)
    band = models.ForeignKey(Band)
    disabled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.band.name


class AlertLog(models.Model):
    user = models.ForeignKey(User)
    band = models.ForeignKey(Band)
    eventskID = models.IntegerField(default=None)
    showDate = models.DateField()
    showURL = models.CharField(max_length=255)
    is_similar = models.BooleanField(default=False)
    send_on = models.DateTimeField()
    has_sent = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.band.name
