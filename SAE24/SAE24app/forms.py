from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from . import models
from django import forms

class CapteursFrom(ModelForm):
    class Meta :
        model = models.Capteurs
        fields = ('nom', 'piece', 'mac')
        labels = {
            'nom' : ('Nom du capteur'),
            'piece' : ('Pièce du capteur'),
            'mac' : ('Adresse MAC du capteur'),
        }
