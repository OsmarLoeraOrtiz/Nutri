# Generated by Django 3.2.23 on 2023-12-17 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nutriologo', '0003_alter_consultorio_nutriologo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultorio',
            name='nutriologo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nutriologo.nutriologo', verbose_name='nutriologo'),
        ),
    ]
