from django.http import JsonResponse
from django.urls import reverse
from evento.models import Notification
from paciente.models import Paciente
from nutriologo.models import Nutriologo
from evento.models import Evento
from django.utils import timezone
from home.views import crear_notificacion

def notifications(request):
    if request.user.is_authenticated:
        notificaciones_no_leidas = 0
        user_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
        notificaciones_leidas = []
        for notificacion in user_notifications:
            if not notificacion.is_read:
                notificaciones_no_leidas += 1
            else:
                notificaciones_leidas.append(notificacion)
        return {'user_notifications': user_notifications, 'notificacionesNoLeidas': notificaciones_no_leidas,'notificacionesLeidas': notificaciones_leidas}
    else:
        return {}
    
def recordatorios_citas(request):
    context_data = {}  # Puedes agregar datos al diccionario según sea necesario
    fecha_actual = timezone.now()
    
    if request.user.is_authenticated:
        try:
            paciente = Paciente.objects.get(user=request.user)
            print("Es paciente")

            citas_proximas = Evento.objects.filter(paciente=paciente)
            for cita in citas_proximas:
                fecha_cita = cita.fecha_inicio
                diferencia = fecha_cita - fecha_actual
                message = f"su cita con {cita.nutriologo.user} es dentro de 24h."
                url = reverse('ver_perfil', kwargs={'username': cita.nutriologo})
                print(f"fecha actual: {fecha_actual}")
                print(f"fecha cita: {fecha_cita}")
                # Verificar si la diferencia es menor o igual a 24 horas
                if 0 <= diferencia.total_seconds() <= 24 * 3600:  # 24 horas en segundos
                    crear_notificacion(paciente.user,"Cita Proxima", message, url)
                    cita.aviso24h = 1
                    cita.save()
                    print("se creo la notificacion")



            # Agrega más datos al diccionario si es necesario para pacientes
        except Paciente.DoesNotExist:
            try:
                nutriologo = Nutriologo.objects.get(user=request.user)
                print("Es nutriologo")

                citas_proximas = Evento.objects.filter(nutriologo=nutriologo)
                for cita in citas_proximas:
                    if cita.aviso24h == 0:
                        fecha_cita = cita.fecha_inicio
                        diferencia = fecha_cita - fecha_actual
                        message = f"su cita con {cita.paciente.user} es dentro de 24h."
                        url = reverse('ver_perfil', kwargs={'username': cita.paciente})

                        # Verificar si la diferencia es menor o igual a 24 horas
                        if 0 <= diferencia.total_seconds() <= 24 * 3600:  # 24 horas en segundos

                            crear_notificacion(nutriologo.user,"Cita Proxima", message, url)
                            cita.aviso24h = 1
                            cita.save()
                    else:
                        pass
           
            except Nutriologo.DoesNotExist:
                # Manejar el caso en que el usuario no sea paciente ni nutriólogo
                pass
    
    return context_data