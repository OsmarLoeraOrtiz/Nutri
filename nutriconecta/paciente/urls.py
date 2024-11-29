from django.contrib import admin
from django.urls import path, include
from .views import *
from login.views import calcular_edad

urlpatterns = [
    path('', PacienteInterfazView.as_view(), name = 'paciente'),
    path('autocompletar-especialidades/', autocompletar_especialidades, name = 'autocompletar-especialidades'),
    path('autocompletar-ubicaciones/', autocompletar_ubicaciones, name = 'autocompletar-ubicaciones'),
    path('filtrar_nutriologos/', nutriologos_por_especialidad_nombre, name = 'filtrar_nutriologos'), 
    path('calcular-edad/', calcular_edad, name='calcular_edad')
]