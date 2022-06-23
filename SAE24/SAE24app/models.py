from django.db import models

class Temperatures(models.Model):
    capteur = models.ForeignKey("Capteurs",null=True, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    temp = models.FloatField()

class Capteurs(models.Model):
    mac = models.CharField(max_length=100)
    piece = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
