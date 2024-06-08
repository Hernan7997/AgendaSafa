# Generated by Django 4.2.13 on 2024-06-05 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgendaContactosApp', '0002_contactos_usuarios_alter_contactos_nota_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='foto',
            field=models.ImageField(default='imagenes/foto_contacto.png', upload_to='imagenes'),
        ),
        migrations.AlterField(
            model_name='contactos',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]