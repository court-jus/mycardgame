# Create your views here.

from django.http import HttpResponse

def accueil(request):
	return HttpResponse("coucou")
