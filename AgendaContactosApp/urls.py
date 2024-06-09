"""
URL configuration for AgendaContactos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('inicio/', inicio, name='inicio'),
    path('sobre_nosotros/', sobre_nosotros, name='sobre_nosotros'),
    path('contactos/', lista_contactos, name='contactos'),
    path('contactos/new/', nuevo_contacto, name='nuevo_contacto'),
    path('contactos/edit/<int:id>/', editar_contacto, name='editar_contacto'),
    path('contactos/borrar/<int:id>/', borrar_contacto, name='borrar_contacto'),
    path('login/', loguear, name='login'),
    path('logout/', desloguear, name='logout'),
    path('perfil/edit/<int:id>/', editar_perfil, name='editar_perfil'),
    path('perfil/', perfil, name='perfil'),
    path('registro/', registro, name='registro'),
    path('admin_usuarios/', lista_usuarios, name='lista_usuarios'),
    path('admin_nuevo_usuario/', nuevo_usuario, name='nuevo_usuario'),
    path('admin_editar_usuario/<int:id>/', editar_usuario, name='editar_usuario'),
    path('admin_borrar_usuario/<int:id>/', borrar_usuario, name='borrar_usuario'),
    path('admin_buscar_usuario/', buscar_usuario, name='buscar_usuario'),
    path('error/', error, name='error'),

]
