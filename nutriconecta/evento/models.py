from django.db import models
from paciente.models import Paciente
from nutriologo.models import Nutriologo
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

# Create your models here.
class Evento(models.Model):
    paciente = models.ForeignKey(Paciente, verbose_name="Paciente", on_delete=models.CASCADE)
    nutriologo = models.ForeignKey(Nutriologo, verbose_name="Nutriologo", on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    titulo = models.CharField(max_length=255)
    motivo = models.CharField(max_length=1000, null=True, blank=True)
    aviso24h = models.IntegerField(default=0)

class SolicitudAgenda(models.Model):
    paciente = models.ForeignKey(Paciente, verbose_name="Paciente", on_delete=models.CASCADE)
    nutriologo = models.ForeignKey(Nutriologo, verbose_name="Nutriologo", on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    titulo = models.CharField(max_length=255)
    motivo = models.CharField(max_length=1000, null=True, blank=True)

    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_url = models.URLField(blank=True, null=True)