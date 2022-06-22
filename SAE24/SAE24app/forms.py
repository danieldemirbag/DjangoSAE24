from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from . import models
from django import forms

class CapteurForm(ModelForm):
    class Meta:
        model = models.Capteur
        fields = ('id')
        labels = {
            'id': _('id'),
        }

class TemperatureForm(ModelForm):
    class Meta:
        model = models.Temperature
        fields = ('id')
        labels = {
            'id': _('id'),
        }