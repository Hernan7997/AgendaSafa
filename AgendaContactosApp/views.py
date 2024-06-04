from django.shortcuts import render

from .models import *


# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def usuario(request):
    return render(request, 'usuario.html')

def sobre_nosotros(request):
    return render(request, 'sobre_nosotros.html')

def contactos(request):
    lista_contactos = Contactos.objects.all()
    return render(request, 'contactos.html', {'lista_contactos': lista_contactos})

