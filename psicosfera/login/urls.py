from django.urls import path, include
from .views import *

urlpatterns = [
    path('', loguear, name = 'login'),
    path('logout', cerrarSesion, name = "logout"),
    path('reestablecer-contraseña', reestablecer_contraseña, name = "reestablecer_contra"),
    path('registro', VRegistro.as_view(), name = "registro"),
    path('registro-usuario', RegistroUsuarioView.as_view(), name = "registro-usuario"),
    path('nuevo-psicologo', NuevoPsicologo.as_view(), name = "nuevo-psicologo"),
    path('nuevo-consultorio', NuevoConsultorio.as_view(), name = "nuevo-consultorio"),
    path('nuevo-paciente', NuevoPaciente.as_view(), name = "nuevo-paciente"),
    
    # # URL para agregar usuario a grupo "Pacientes"
    # path('agregar-paciente', agregar_paciente, name='agregar-paciente'),
    # # URL para agregar usuario a grupo "Psicólogos"
    # path('agregar-psicologo', agregar_psicologo, name='agregar-psicologo'),
    # # URL para agregar usuario a grupo "Usuarios-Registrados"
    # path('usuario-registrado', usuario_registrado, name='usuario-registrado'),
]
 