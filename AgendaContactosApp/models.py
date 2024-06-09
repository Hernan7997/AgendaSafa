from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.

# clase enumerada para poder asignar los roles
class Rol(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrador'
    PERSONA = 'PERSONA', 'Persona'


# clase gestor de usuarios
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            return ValueError('Es necesario  el email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# AbstractBaseUser utiliza la herencias de django para usar los campos predeterminados de django
class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=25, choices=Rol.choices, default=Rol.PERSONA)
    # estos campos son predeterminados de django que pisamos para configurarlos a nuestro gusto
    # is_active es para habilitar al usuario diciendo que esta activo
    is_active = models.BooleanField(default=True)
    # is_staff es default false para que no cree un usuario como staff
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # Campos obligatorios, uno para loguear y otro simplemente obligatorio
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    # Metodo para guardar el usuario
    def save(self, *args, **kwargs):
        # Si el usuario es nuevo, se crea una nueva persona asociada a él
        if not self.pk:
            super(User, self).save(*args, **kwargs)
            Persona.objects.create(user=self)
        # Si el usuario ya existe, se guarda normalmente
        else:
            super(User, self).save(*args, **kwargs)

    # Metodo para obtener el rol del usuario

class Persona(models.Model):
    # Variables
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=255)
    telefono = models.CharField(max_length=12)
    # fecha de nacimiento con el valor por defecto de la fecha actual
    fecha_nacimiento = models.DateField(default=date.today)
    foto = models.ImageField(upload_to='foto_usuario', default='foto_usuario/default.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre


# Creacion de clase Contactos en herencia al modelo de Django
class Contactos(models.Model):
    # Variables
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=255)
    telefono = models.CharField(max_length=12)
    email = models.EmailField(default='example@gmail.com')
    nota = models.CharField(max_length=100, default='Sin nota', null=True)
    foto = models.ImageField(upload_to='foto_contacto', default='foto_usuario/default.png')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre + ' ' + self.apellidos
