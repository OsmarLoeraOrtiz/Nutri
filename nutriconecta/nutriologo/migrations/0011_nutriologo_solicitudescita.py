# Generated by Django 3.2.23 on 2024-02-03 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutriologo', '0010_nutriologo_solicitudes'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutriologo',
            name='solicitudesCita',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
