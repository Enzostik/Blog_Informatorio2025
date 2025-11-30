from django.http.request import HttpRequest
from django.shortcuts import render

# Modelos de las publicaciones
from .models import Publication

# Create your views here.
def noticias(request:HttpRequest):
    all_publications = Publication.objects.all().order_by('-creation_date')
    return render(request, 'noticias/noticias.html', context={'publicaciones': all_publications})

def ver_noticia(request:HttpRequest, id_noticia:int):
    publication = Publication.objects.get(pk=id_noticia)
    return render(request, 'noticias/ver_noticia.html', context={'publication': publication})