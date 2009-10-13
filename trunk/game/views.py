# -*- coding: utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from game.models import *

def accueil(request):
    j1 = get_object_or_404(Joueur,name = "Ghislain")
    j2 = get_object_or_404(Joueur,name = "Toto")
    return render_to_response("game.html", {"me":j1,"him":j2})