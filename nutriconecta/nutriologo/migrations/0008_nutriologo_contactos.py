# Generated by Django 3.2.23 on 2024-01-09 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutriologo', '0007_nutriologo_correo_verificado'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutriologo',
            name='contactos',
            field=models.JSONField(blank=True, null=True),
        ),
    ]