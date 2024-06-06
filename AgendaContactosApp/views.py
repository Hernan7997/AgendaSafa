from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from .models import *


# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def perfil(request):
    return render(request, 'perfil.html')

def sobre_nosotros(request):
    return render(request, 'sobre_nosotros.html')

def lista_contactos(request):
    listacontactos = Contactos.objects.filter(user=request.user)
    return render(request, 'contactos.html', {'lista_contactos': listacontactos})

#Los GET son para crear un formulario vacio
#los POST son para enviar los datos de la base de datos

def nuevo_contacto(request):
    # Si el metodo es GET, se muestra el formulario vacio
    if request.method == 'GET':
        return render(request, 'nuevo_contacto.html')
    # Si el metodo es POST, aparecen los datos del contacto seleccionado
    else:
        nuevo = Contactos()
        nuevo.nombre = request.POST.get('nombre')
        nuevo.apellidos = request.POST.get('apellidos')
        nuevo.telefono = request.POST.get('telefono')
        nuevo.email = request.POST.get('email')
        nuevo.nota = request.POST.get('nota')
        nuevo.save()
        return redirect('/AgendaContactos/contactos')


def borrar_contacto(request, id):
    contacto = Contactos.objects.get(id= id)
    contacto.delete()
    return redirect('/AgendaContactos/contactos')

# Igual que crear un contacto solo que con la diferencia que solicitas el id del contacto a editar
def editar_contacto(request, id):
    contacto = Contactos.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'nuevo_contacto.html', {'contacto': contacto})
    else:
        contacto.nombre = request.POST.get('nombre')
        contacto.apellidos = request.POST.get('apellidos')
        contacto.telefono = request.POST.get('telefono')
        contacto.email = request.POST.get('email')
        contacto.nota = request.POST.get('nota')
        contacto.save()
        return redirect('/AgendaContactos/contactos')

def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html')
    else:
        # recogemos los datos del usuario
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('repeatPassword')

        errors = []

        # Los errores podemos realizarlos por javaScript para introducir javaScript en el proyecto

        # Validacion de contraseñas
        if password != password2:
            errors.append("Las contraseñas no coinciden")

        # Validacion de email con otros usuarios
        existe_usuario = User.objects.filter(username=username).exists()
        if existe_usuario:
            errors.append("Ya existe un usuario con ese nombre de usuario")
        existe_email = User.objects.filter(email=email).exists()
        if existe_email:
            errors.append("Ya existe un usuario con ese mismo email")


        if len(errors) != 0:
            return render(request, 'registro.html', {"errores":errors, "username": username, "email": email})
        else:
            # Crear usuario
            usuario = User.objects.create(username=username, password=make_password(password), email=email)
            usuario.save()

            # Redirigir al logging
            return redirect('/AgendaContactos/login')

def loguear(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate busca el usuario en la base de datos
        user = authenticate(request, username=username, password=password)

        # Si encuentra el usuario se loguea // login es un metodo importado predefinido de django junto con authenticate
        if user is not None:
            login(request, user)

            # Redireccionar tras login existoso
            return redirect('inicio')

        else:
            # Mensaje de error si falla
            return render(request, 'login.html', {"error": "No se ha podido iniciar sesión"})

    # Mostrar formulario de login para metodo GET
    return render(request,  'login.html')

def desloguear(request):
    logout(request)
    return redirect('/AgendaContactos/login')

# @check_user_role('ADMIN')
def lista_usuarios(request):
    listausuarios = User.objects.all()
    return render(request, 'admin_usuarios.html', {'lista_usuarios': listausuarios})