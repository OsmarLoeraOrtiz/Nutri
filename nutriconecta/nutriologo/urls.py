from django.contrib import admin
from django.urls import path
from .views import *
from paciente.views import datos_paciente
from home.views import aceptar_solicitud_cita
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', interfaz_nutriologo, name = 'interfaz'),
    path('diario_nutriologo/', diario_nutriologo, name='diario_nutriologo'), # type: ignore
    path('datos_paciente/', datos_paciente, name='datos_paciente'),
    path('datos_nutriologo/', datos_nutriologo, name='datos_nutriologo'),
    path('guardar_personales/', guardar_diario, name='guardar_personales'),
    path('actualizar_nutriologo/', actualizar_nutriologo, name='actualizar_nutriologo'),
    path('guardar_cita/', guardar_cita, name='guardar_cita'),
    path('aceptar_solicitud_cita/', aceptar_solicitud_cita, name='aceptar_solicitud_cita'),
    path('guardar_notas/', guardar_notas, name='guardar_notas'),
    path('obtener_citas/', obtener_citas, name='obtener_citas'),
    path('obtener_solicitud_citas/', obtener_solicitud_citas, name='obtener_solicitud_citas'),
    path('obtener_pacientes/', obtener_pacientes, name='obtener_pacientes'),
    path('eliminar_cita/', eliminar_cita, name='eliminar_cita'),
    path('eliminar_solicitud_cita/', eliminar_solicitud_cita, name='eliminar_solicitud_cita'),
    path('paciente_pdf/<int:paciente_id>', paciente_pdf, name='paciente_pdf'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)