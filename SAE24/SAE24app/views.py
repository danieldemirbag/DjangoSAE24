from django.shortcuts import render, HttpResponseRedirect,HttpResponse
from django.http import Http404,FileResponse
from . import models
from .forms import *
import mimetypes
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mysql.connector

# Create your views here.

def index(request):
    raise Http404("TKT CA MARCHE")

def display_all_data(request):
    temp = models.Temperatures.objects.all()
    capteurs = models.Capteurs.objects.all()
    return render(request, "disp_all_data.html",{"data":capteurs,"temp":temp})


def update(request, id):
    content = models.Capteurs.objects.get(pk=id)
    form = CapteursFrom()
    form.fields['mac'].widget.attrs['readonly'] = True
    form.fields['mac'].initial = content.mac
    return render(request, "update.html", {"form": form, "id": id})


def updatetraitement(request, id):
    form = CapteursFrom(request.POST)
    if form.is_valid():
        capteurs = form.save(commit=False)
        capteurs.id = id
        capteurs.save()
        return HttpResponseRedirect('/get_temp/display_all/')
    else:
        return render(request, "disp_all_data.html", {"form": form, "id": id})

def filter(request):
    liste_retenus = []
    if request.method == "POST":
        capteur_mac = request.POST['mac']
        date = request.POST['date']
        date = "-".join(date.split("/")[::-1])
        time = request.POST['time']
        if capteur_mac == "" and date == "" and time == "":
            return render(request, "filter.html")
        temp = models.Temperatures.objects.all()
        for i in temp:
            test = True
            if capteur_mac!="":
                if i.capteur.mac != capteur_mac:
                    test = False
            if date!="":
                if str(i.date) != str(date):
                    test = False
            if time!="":
                if str(i.time) != str(time):
                    test = False
            if test:
                liste_retenus.append(i)
        return render(request, "disp_all_data.html", {"data":models.Capteurs.objects.all() , "temp": liste_retenus})


    else:
        return render(request, "filter.html")

def gen_file():
    big_dict = {}
    temp = models.Temperatures.objects.all()
    capteurs = models.Capteurs.objects.all()
    for i in capteurs:
        if i.mac not in big_dict.keys():
            big_dict[i.mac]={"piece":i.piece,"nom":i.nom,"temps":[]}
    for i in temp:
        if i.capteur.mac in big_dict.keys():
            big_dict[i.capteur.mac]["temps"].append({"date":str(i.date),"time":str(i.time),"temp":i.temp})
    with open("./jsonfiles/backup.json","w") as file:
        json.dump(big_dict,file)


def export(request):
    gen_file()
    filepath = f"./jsonfiles/backup.json"
    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % "backup.json"
    return response

def image(request):
    temp = models.Temperatures.objects.all()
    capteurs = models.Capteurs.objects.all()
    y=[float(i.temp) for i in temp  if i.capteur.id==1]
    x=[float(str(i.time).split(":")[0]+"."+str(i.time).split(":")[1]) for i in temp if i.capteur.id==1]
    y2=[float(i.temp) for i in temp  if i.capteur.id==2]
    return render(request, "image.html",{"x":x,"y2":y2,"y":y})

def graph(request):
    return HttpResponseRedirect('/get_temp/image/')
