from django.db import models

# Create your models here.
class Usuarios(models.Model):
    # Variables
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=255)
    telefono = models.CharField(max_length=12)
    email = models.EmailField()
    fecha_nacimiento = models.DateField()


    def __str__(self):
        return self.nombre


# Creacion de clase Contactos en herencia al modelo de Django
class Contactos(models.Model):
    # Variables
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=255)
    telefono = models.CharField(max_length=12)
    email = models.EmailField()
    nota = models.CharField(max_length=100,null=True, default='Sin nota')
    usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre + ' ' + self.apellidos
