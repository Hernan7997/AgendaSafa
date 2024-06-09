from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .decorator import check_user_logged, check_user_role
from .models import *


# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')


def sobre_nosotros(request):
    return render(request, 'sobre_nosotros.html')


@check_user_logged()
def lista_contactos(request):
    listacontactos = Contactos.objects.filter(user=request.user)
    return render(request, 'contactos.html', {'lista_contactos': listacontactos})


# Los GET son para crear un formulario vacio
# los POST son para enviar los datos de la base de datos

@check_user_logged()
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
        nuevo.user = request.user
        nuevo.save()
        return redirect('contactos')


@check_user_logged()
def borrar_contacto(request, id):
    contacto = Contactos.objects.get(id=id)
    contacto.delete()
    return redirect('contactos')


# Igual que crear un contacto solo que con la diferencia que solicitas el id del contacto a editar
@check_user_logged()
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

        # Guardar la foto si se proporciona
        if 'foto' in request.FILES:
            # Comprobar que el archivo es una imagen
            foto = request.FILES['foto']
            # Comprobar que el archivo es una imagen
            if foto.content_type not in ['image/png', 'image/jpeg', 'image/jpg']:
                return render(request, 'nuevo_contacto.html',
                              {'contacto': contacto, 'error': 'El archivo debe ser una imagen PNG o JPEG'})
            # Guardar la imagen si es válida
            contacto.foto = foto
        # No hace falta un else porque si no se cumple la condicion se mantendra la foto que ya tenia

        contacto.save()
        return redirect('contactos')


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
            # Devolver errores en formato JSON para que JavaScript los muestre
            return render(request, 'registro.html', {"errores": errors})

        else:
            # Crear usuario
            usuario = User.objects.create(username=username, password=make_password(password), email=email)
            usuario.save()

            # Redirigir al logging
            return redirect('login')


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
    return render(request, 'login.html')


def desloguear(request):
    logout(request)
    return redirect('login')


@check_user_logged()
def perfil(request):
    user = request.user
    persona = Persona.objects.get(user=user)

    return render(request, 'perfil.html', {'persona': persona})


@check_user_logged()
def editar_perfil(request, id):
    # Coger la persona que se va a editar
    persona = Persona.objects.get(id=id)
    if request.user.id != persona.user.id:
        return redirect('error')

    if request.method == 'POST':
        persona.nombre = request.POST.get('nombre')
        persona.apellidos = request.POST.get('apellidos')
        persona.telefono = request.POST.get('telefono')
        persona.fecha_nacimiento = request.POST.get('fecha_nacimiento')

        # Guardar la foto si se proporciona
        if 'foto' in request.FILES:
            # Comprobar que el archivo es una imagen
            foto = request.FILES['foto']
            # Comprobar que el archivo es una imagen
            if foto.content_type not in ['image/png', 'image/jpeg', 'image/jpg']:
                return render(request, 'editar_perfil.html',
                              {'persona': persona, 'error': 'El archivo debe ser una imagen PNG o JPEG'})
            # Guardar la imagen si es válida
            persona.foto = foto
        # No hace falta un else porque si no se cumple la condicion se mantendra la foto que ya tenia

        persona.save()
        return redirect('perfil')
    else:
        return render(request, 'editar_perfil.html', {'persona': persona})


@check_user_role('ADMIN')
def lista_usuarios(request):
    listausuarios = User.objects.all()
    return render(request, 'admin_usuarios.html', {'lista_usuarios': listausuarios})


@check_user_role('ADMIN')
def nuevo_usuario(request):
    # aqui estoy cogiendo los roles para mostrarlos pero
    # solo estoy cogiendo el campo 2 de la tupla, es decir, la descripcion
    roles = [choice[0] for choice in Rol.choices]
    errores = []
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        rol = request.POST.get('rol')

        if not username:
            errores.append('El nombre de usuario es obligatorio')
        if not email:
            errores.append('El email es obligatorio')
        if not rol or rol == 'predeterminado':
            errores.append('El rol es obligatorio, por favor seleccione uno')

        # Verificar si el nombre de usuario o el correo electrónico ya están en uso
        if User.objects.filter(username=username).exists():
            errores.append('El nombre de usuario ya está en uso')
        if User.objects.filter(email=email).exists():
            errores.append('El correo electrónico ya está en uso')

        if not errores:
            # Crear y guardar el nuevo usuario si no hay errores
            nuevo_usuario = User(username=username, email=email, rol=rol)
            nuevo_usuario.save()

    return render(request, 'admin_nuevo_usuario.html', {'roles': roles, 'errores': errores})


@check_user_role('ADMIN')
def editar_usuario(request, id):
    usuario = User.objects.get(id=id)
    roles = [choice[0] for choice in Rol.choices]
    errores = []

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        rol = request.POST.get('rol')

        if not username:
            errores.append('El nombre de usuario es obligatorio')
        if not email:
            errores.append('El email es obligatorio')
        if not rol or rol == 'predeterminado':
            errores.append('El rol es obligatorio, por favor seleccione uno')

        # Verificar si el correo electrónico ya está en uso
        if User.objects.filter(email=email).exclude(id=usuario.id).exists():
            errores.append('El correo electrónico ya está en uso')

        if not errores:
            usuario.username = username
            usuario.email = email
            usuario.rol = rol

            # Guardar el usuario si no hay errores
            try:
                usuario.save()
            except ValidationError as e:
                errores.append(str(e))
            else:
                return redirect('lista_usuarios')

    return render(request, 'admin_nuevo_usuario.html', {'usuario': usuario, 'roles': roles, 'errores': errores})


@check_user_role('ADMIN')
def borrar_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    return redirect('lista_usuarios')


@check_user_role('ADMIN')
def buscar_usuario(request):
    # Obtenemos el nombre de usuario del request
    username = request.GET.get('username')
    if username:
        # Buscar usuarios que coincidan
        usuarios = User.objects.filter(username__icontains=username)
    else:
        # Si no se proporciona un nombre de usuario, obtener todos los usuarios
        usuarios = User.objects.all()

    return render(request, 'admin_usuarios.html', {'lista_usuarios': usuarios})


def error(request):
    return render(request, 'error.html')
