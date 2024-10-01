from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from psicologo.especialidades import ESPECIALIDADES_CHOICES_2

ESP_CHOICES = ESPECIALIDADES_CHOICES_2
SEXO_CHOICES = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('O', 'Otro'),
)


# Modelo de psicologo
class Psicologo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=254, null=True, blank=False, verbose_name="Descripción")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento", null=False, blank=False)
    edad = models.PositiveIntegerField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=False, blank=False)
    telefono = models.CharField(max_length=10, null=False, blank=False)
    ubicacion = models.CharField(max_length=200, verbose_name="Ubicación", blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='psicologos_foto_perfil/', blank=True) #mover al eliminar los antiguos usuarios blank=False, null=False
    fecha_registro = models.DateTimeField(auto_now_add=True)
    correo_verificado = models.BooleanField(default=False)
    notificaciones_cambios = models.BooleanField(default=True)
    notificaciones_servicios = models.BooleanField(default=True)
    notificaciones_promociones = models.BooleanField(default=False)
    cedula = models.CharField(max_length=8, null=False, blank=False)  #mover al eliminar los antiguos usuarios blank=False, null=False
    especialidad = models.CharField(max_length=50, choices=ESP_CHOICES, null=False, blank=False)
    institucion_otorgamiento = models.CharField(max_length=200, verbose_name="Institución de otorgamiento", null=False, blank=False)
    fecha_obtencion = models.DateTimeField(auto_now_add=True, null=True)
    curriculum = models.FileField(upload_to='curriculum_psicologo/', blank=True, null=True)  #mover al eliminar los antiguos usuarios blank=False, null=False
    certificado = models.FileField(upload_to='certificados_psicologos/', blank=True, null=True) #mover al eliminar los antiguos usuarios blank=False, null=False
    identificacion_oficial = models.FileField(upload_to='identificacion_psicologos/', blank=True, null=True) #mover al eliminar los antiguos usuarios blank=False, null=False
    enlace_pagina_web = models.URLField(blank=True, null=True)
    enlace_facebook = models.URLField(blank=True, null=True)
    enlace_instagram = models.URLField(blank=True, null=True)
    enlace_linkedin = models.URLField(blank=True, null=True)
    diario = RichTextField(blank=True, null=True)
    contactos = models.JSONField(blank=True, null=True)
    solicitudes = models.JSONField(blank=True, null=True)
    solicitudesCita = models.JSONField(blank=True, null=True)
    
    

    def __str__(self):
        return f"{self.user}"

# Modelo de consultorio de los psicologos
class Consultorio(models.Model):
    psicologo = models.OneToOneField('Psicologo', verbose_name='psicologo', on_delete=models.CASCADE)
    direccion = models.CharField(max_length=250,verbose_name="Dirección", null=False, blank=False)
    horario_apertura = models.TimeField(blank=True, null=True)
    horario_cierre = models.TimeField(blank=True, null=True)
    costo_consulta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo de Consulta", blank=True, null=True)
    def __str__(self):
        return f"{self.psicologo}"

    