# Generated by Django 3.2.23 on 2024-01-06 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psicologo', '0006_psicologo_ubicacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='psicologo',
            name='correo_verificado',
            field=models.BooleanField(default=False),
        ),
    ]