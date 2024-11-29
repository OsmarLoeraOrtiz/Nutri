# Generated by Django 3.2.23 on 2023-12-13 20:48

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Nutriologo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=8)),
                ('edad', models.PositiveIntegerField()),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=1)),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('especialidad', models.CharField(choices=[('clinica', 'Nutrición Clínica'), ('deportiva', 'Nutrición Deportiva'), ('infantil', 'Nutrición Infantil'), ('geriatrica', 'Nutrición Geriátrica'), ('comunitaria', 'Nutrición Comunitaria'), ('oncologica', 'Nutrición Oncológica'), ('renal', 'Nutrición Renal'), ('vegetariana_vegana', 'Nutrición Vegetariana y Vegana'), ('funcional', 'Nutrición Funcional'), ('educacion_alimentaria', 'Educación Alimentaria'), ('metabolica', 'Nutrición Metabólica'), ('trastornos_conducta', 'Nutrición en Trastornos de la Conducta Alimentaria'), ('enfermedades_cronicas', 'Nutrición en Enfermedades Crónicas'), ('seguridad_alimentaria', 'Seguridad Alimentaria'), ('embarazo', 'Nutrición y Embarazo'), ('publica', 'Nutrición Pública'), ('nutriogenomica', 'Nutriogenómica'), ('precision', 'Nutrición de Precisión'), ('bariatrica', 'Nutrición Bariátrica'), ('otra_especialidad', 'Otra Especialidad')], max_length=50)),
                ('telefono', models.CharField(max_length=10)),
                ('institucion_otorgamiento', models.CharField(max_length=200, verbose_name='Institución de otorgamiento')),
                ('fecha_obtencion', models.DateTimeField(auto_now_add=True, null=True)),
                ('curriculum', models.FileField(blank=True, null=True, upload_to='curriculum_nutriologo/')),
                ('foto_perfil', models.ImageField(blank=True, upload_to='nutriologos_foto_perfil/')),
                ('certificado', models.FileField(blank=True, null=True, upload_to='certificados_nutriologos/')),
                ('identificacion_oficial', models.FileField(blank=True, null=True, upload_to='identificacion_nutriologos/')),
                ('enlace_pagina_web', models.URLField(blank=True, null=True)),
                ('enlace_facebook', models.URLField(blank=True, null=True)),
                ('enlace_instagram', models.URLField(blank=True, null=True)),
                ('enlace_linkedin', models.URLField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('diario', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('descripcion', models.CharField(max_length=254, null=True, verbose_name='Descripción')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Consultorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=250, verbose_name='Dirección')),
                ('horario_atencion', models.TimeField(blank=True, null=True)),
                ('nutriologo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutriologo.nutriologo', verbose_name='Consultorio')),
            ],
        ),
    ]