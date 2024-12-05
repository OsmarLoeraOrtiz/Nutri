from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from paciente.views import datos_paciente
from nutriologo.views import codigoANombre, datos_nutriologo
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from nutriologo.models import Consultorio, Nutriologo
from paciente.models import Paciente
from evento.models import Notification, Evento, SolicitudAgenda
import base64
from nutriologo.forms import FormNutriologo, FormConsultorio
from paciente.forms import FormPaciente
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from nutriconecta.settings import MEDIA_ROOT
from datetime import datetime
        
class Home(TemplateView):
    def get_template_names(self):
        if self.request.user.groups.filter(name='Nutriologos').exists(): # type: ignore
            return ['homeNutriologo.html']
        else:
            return ['home.html']
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

def contacto(request):
    return render(request, 'contacto.html')

@login_required
def actualizar_password(request):
    if request.method == 'POST':
        password_actual = request.POST['password_actual'] 
        nueva_password = request.POST['nueva_password']
        confirmar_password = request.POST['confirmar_password']
        # Verificar la password actual del usuario
        user = authenticate(request, username=request.user.username, password=password_actual)
        if user is not None:
            # La password actual es válida
            if nueva_password == confirmar_password:
                # Las passwords coinciden, proceder con el cambio de password
                request.user.set_password(nueva_password)
                request.user.save()
                perfil_url = reverse('perfil')
                message = "Contraseña actualizada exitosamente."
                crear_notificacion(user,"Seguridad", message,perfil_url)
                messages.success(request, message)
                return redirect('login')
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
                return redirect('perfil')
        else:
            messages.error(request, 'La contraseña actual es incorrecta.')
            return redirect('perfil')
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405) 

def enviar_correo(asunto,correo, mensaje):
    email_origen = 'yodacholo@gmail.com'
    recipient_list = [correo]

    email = EmailMessage(asunto, mensaje, email_origen, recipient_list)
    email.send()
    print(correo)
    return print("Correo enviado:"+ " "+ asunto)
    
    
def enviar_correo_confirmacion(request):
    # Generar token de confirmación
    usuario = request.user
    token = default_token_generator.make_token(usuario)
    
    # Construir la URL de confirmación
    url_confirmacion = reverse('confirmar_correo', args=[usuario.pk, token])
    enlace_confirmacion = f'http://{settings.SITE_DOMAIN}{url_confirmacion}'
    mensaje = f'Haz clic en el siguiente enlace para confirmar tu correo: {enlace_confirmacion}'
    asunto = 'Confirma tu correo'
    
    enviar_correo(asunto,usuario.email,mensaje)
    return redirect('perfil')



def confirmar_correo(request, pk, token):
    usuario = get_object_or_404(User, pk=pk)
    
    try:
        usuario = usuario.paciente
    except:
        usuario = usuario.nutriologo
        
    if default_token_generator.check_token(usuario.user, token):
        usuario.correo_verificado = True
        usuario.save()
        return redirect('perfil')
    else:
        return HttpResponse('Enlace de confirmación no válido.')
    
def ajuste_notificaciones(request):
    if request.method == 'POST':
        try:
            usuario = request.user.paciente
        except:
            usuario = request.user.nutriologo
        cambios = request.POST.get('cambios') == 'on'
        servicios = request.POST.get('servicios') == 'on'
        promociones = request.POST.get('promociones') == 'on'

        print(cambios, servicios, promociones)
        
        usuario.notificaciones_cambios = cambios
        usuario.notificaciones_servicios = servicios
        usuario.notificaciones_promociones = promociones
        usuario.save()
        perfil_url = reverse('perfil')
        crear_notificacion(request.user,"Cambios", "Se han guardado tus cambios correctamente.",perfil_url)

        return redirect('actualizacion_exitosa')
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405) 
    
     
def crear_notificacion(user,asunto, mensaje, url):
    Notification.objects.create(user=user, mensaje=mensaje, notification_url=url)
    try:
        usuario = user.paciente
    except:
        usuario = user.nutriologo

    if asunto == "Cambios" and usuario.notificaciones_cambios:
        enviar_correo(asunto,user.email, mensaje) 
    elif asunto == "Servicios" and usuario.notificaciones_servicios:
        enviar_correo(asunto,user.email, mensaje)
    elif asunto == "Promociones" and usuario.notificaciones_promociones:
        enviar_correo(asunto,user.email, mensaje)
    elif asunto == "Seguridad":
        enviar_correo(asunto,user.email, mensaje)
    elif asunto == "Amistad":
        enviar_correo(asunto,user.email, mensaje)
    elif asunto == "Agendar Cita":
        enviar_correo(asunto,user.email, mensaje)
    elif asunto == "Cita Proxima":
        enviar_correo(asunto,user.email, mensaje)
    else:
        pass

@login_required
def aceptar_solicitud_cita(request):
    if request.method == 'POST':
        try:
            solicitud = SolicitudAgenda.objects.get(id=request.POST.get('id'))
            paciente = solicitud.paciente
            nutriologo = solicitud.nutriologo
            titulo = solicitud.titulo
            fecha_inicio = solicitud.fecha_inicio
            fecha_fin = solicitud.fecha_fin
            motivo = solicitud.motivo
            solicitud.delete()

             # Crear un nuevo evento con la información de la solicitud
            cita = Evento(paciente=paciente, nutriologo=nutriologo, titulo=titulo, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, motivo=motivo)
            cita.save()

            asunto = "Agendar Cita"
            mensaje = f"{nutriologo} ha aceptado tu cita para el día {fecha_inicio}"
            url = reverse('ver_perfil', kwargs={'username': nutriologo})
            crear_notificacion(paciente.user,asunto,mensaje,url)
            
            return JsonResponse({'mensaje': 'Cita guardada con éxito'})
        except Evento.DoesNotExist:
            return JsonResponse({'mensaje': 'La cita no existe'}, status=404)
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)
    
def eliminar_solicitud_cita_nutriologo(request):
    if request.method == 'POST':
        try:
            cita = SolicitudAgenda.objects.get(id=request.POST.get('id'))
            paciente = cita.paciente
            nutriologo = cita.nutriologo
            fecha_inicio = cita.fecha_inicio

            cita.delete()

            asunto = "Agendar Cita"
            mensaje = f"{nutriologo} ha rechazado tu cita para el día {fecha_inicio}"
            url = reverse('ver_perfil', kwargs={'username': nutriologo})
            crear_notificacion(paciente.user,asunto,mensaje,url)

            return JsonResponse({'mensaje': 'Cita eliminada con éxito'})
        except Evento.DoesNotExist:
            return JsonResponse({'mensaje': 'La cita no existe'}, status=404)
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)
    
@login_required   
def obtener_motivo(request):
    if request.method == 'GET':
        cita_id = request.GET.get('id')
        cita = get_object_or_404(SolicitudAgenda, id=cita_id)
        motivo = cita.motivo
        return JsonResponse({'mensaje': motivo})
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)
        
    
def marcar_notificacion_leida(request):
    if request.method == 'POST':
        notification_url = request.POST.get('notification_url', '')
        notification_id = request.POST.get('notification_id', '')
        if notification_id:
            try:
                # Obtén la notificación basada en la URL
                notification = Notification.objects.get(id=notification_id, user=request.user)
                notification.is_read = True
                notification.save()
                return JsonResponse({'success': True, 'redirect_url': notification_url})
            except Notification.DoesNotExist:
                pass

    return JsonResponse({'success': False})

def perfil(request):
    if request.user.groups.filter(name='Nutriologos').exists():
        nutriologo=Nutriologo.objects.get(user=request.user)
        consultorio = Consultorio.objects.get(nutriologo=nutriologo)
        datos = {
            'direccion' : consultorio.direccion,
            'correo_verificado' : nutriologo.correo_verificado
        }   
        
        ajuste_notificaciones = {
            "cambios":nutriologo.notificaciones_cambios,
            "servicios":nutriologo.notificaciones_servicios,
            "promociones":nutriologo.notificaciones_promociones,
        }
        formConsultorio = FormConsultorio(instance=consultorio)
        formNutriologo = FormNutriologo(instance=nutriologo)
        return render(request, 'perfil_nutriologo_privado.html', {'formNutriologo': formNutriologo, 'formConsultorio': formConsultorio,'usuario': datos, 'ajuste_notificaciones': ajuste_notificaciones})
    elif request.user.groups.filter(name='Pacientes').exists():
        paciente=Paciente.objects.get(user=request.user)
        ajuste_notificaciones = {
            "cambios":paciente.notificaciones_cambios,
            "servicios":paciente.notificaciones_servicios,
            "promociones":paciente.notificaciones_promociones,
        }
        form = FormPaciente(instance=paciente)
        return render(request, 'perfil_paciente.html', {'form': form, 'correo_verificado' : paciente.correo_verificado,'ajuste_notificaciones': ajuste_notificaciones})
    else:
        return redirect('login')
    
def exito_actualizacion(request):
    return HttpResponseRedirect(reverse('perfil') + '?success=true')

def enviar_solicitud(request, username):
    #Solo el paciente puede enviar solicitud
    user = get_object_or_404(User, username=username)
    paciente = get_object_or_404(Paciente, user=request.user)
    paciente_user = paciente.user.username
    asunto = "Amistad"
    mensaje = f"{paciente_user} te ha enviado una solicitud."
    url = reverse('ver_perfil', kwargs={'username': paciente})
    crear_notificacion(user,asunto,mensaje,url)
    try:
        nutriologo = Nutriologo.objects.get(user=user)
        if not nutriologo.solicitudes:
            nutriologo.solicitudes = []
        if paciente.id not in nutriologo.solicitudes:
            nutriologo.solicitudes.append(paciente.id)
        nutriologo.save()

        print(f"Solicitud envviada a {nutriologo.id}: ")
        print(f"Solicitudes de {nutriologo.id}: {nutriologo.solicitudes}")
    except Nutriologo.DoesNotExist:
        # Si el nutriologo no existe, devolvemos un mensaje de error
        return JsonResponse({"error": "El nutriologo no existe"})

    # Respuesta JSON para confirmar el éxito
    return JsonResponse({"message": "Solicitud enviada exitosamente"})

@login_required
def agendar_cita(request, username):
    # Obtener el usuario basado en el username
    user = get_object_or_404(User, username=username)
    
    # Intentar obtener el perfil de nutriologo para el usuario
    if request.method == 'POST':
        try:
            nutriologo = Nutriologo.objects.get(user=user)
            try:
                paciente = Paciente.objects.get(user=request.user)
            except Paciente.DoesNotExist:
                return JsonResponse({'mensaje': 'Paciente no encontrado.'}, status=404)
            
            titulo = request.POST.get('titulo')
            motivo = request.POST.get('motivo')
            fecha_inicio = request.POST.get('start').replace('-06:00', "")
            fecha_fin = request.POST.get('end').replace('-06:00', "")

            cita = SolicitudAgenda(paciente=paciente, nutriologo=nutriologo, titulo=titulo, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, motivo=motivo)
            cita.save()
            print("------CITA-----")
            print(cita)
            print("---------------")
            notificacion_cita(paciente, nutriologo)

            print(cita)
            # Agrega un retorno específico para el éxito en el método POST
            return JsonResponse({'mensaje': 'Cita agendada correctamente'})
        except Nutriologo.DoesNotExist:
            return JsonResponse({'mensaje': 'El nutriologo no existe'}, status=404)  # El usuario no es un nutriologo, continuar
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)  

def notificacion_cita(paciente, nutriologo):
    _nutriologo = nutriologo
    _paciente = paciente
    paciente_user = _paciente.user.username
    asunto = "Agendar Cita"
    mensaje = f"{paciente_user} te ha solicitado agendar una cita."
    url = reverse('interfaz')
    crear_notificacion(_nutriologo.user,asunto,mensaje,url)
    print("Se creo la notificacion")
    # Respuesta JSON para confirmar el éxito
    return JsonResponse({"message": "Solicitud enviada exitosamente"})

def agregar_contacto(request, username):
    #La idea general es que obtenga al usuario actual (debe ser paciente) y al nutriologo que es el username de la URL
    user = get_object_or_404(User, username=username)
    nutriologo = get_object_or_404(Nutriologo, user=request.user)
    try:
        paciente = Paciente.objects.get(user=user)
     
        if not paciente.contactos:
            paciente.contactos = []
        if not paciente.solicitudes:
            paciente.solicitudes = []
        if nutriologo.id not in paciente.contactos:
            paciente.contactos.append(nutriologo.id)
            if nutriologo.id in paciente.solicitudes:
                paciente.solicitudes.remove(nutriologo.id) #Se elimina la solicitud
        paciente.save()

        if not nutriologo.contactos:
            nutriologo.contactos = []
        if not nutriologo.solicitudes:
            nutriologo.solicitudes = []
        if paciente.id not in nutriologo.contactos:
            nutriologo.contactos.append(paciente.id)
            if paciente.id in nutriologo.solicitudes:
                nutriologo.solicitudes.remove(paciente.id) #Se elimina la solicitud
        nutriologo.save()

        print(f"Contactos paciente {paciente.id}: ")
        print(paciente.contactos)
        print(f"Contactos nutriologo: {nutriologo.id}: ")
        print(nutriologo.contactos)
        nutriologo_user = nutriologo.user.username
        asunto = "Amistad"
        mensaje = f"{nutriologo_user} ha aceptado tu solicitud."
        url = reverse('ver_perfil', kwargs={'username': nutriologo})
        crear_notificacion(user,asunto,mensaje,url)

        # Respuesta JSON para confirmar el éxito
        return JsonResponse({"message": "Contacto agregado exitosamente"})

    except Nutriologo.DoesNotExist:
        # Si el nutriologo no existe, devolvemos un mensaje de error
        return JsonResponse({"error": "El nutriologo no existe"})
    except Paciente.DoesNotExist:
        # Si el paciente no existe, devolvemos un mensaje de error
        return JsonResponse({"error": "El paciente no existe"})
 
def eliminar_contacto(request, username):
    #La idea general es que obtenga al usuario actual (debe ser paciente) y al nutriologo que es el username de la URL
    user = get_object_or_404(User, username=username)
    
    try:
        nutriologo = Nutriologo.objects.get(user=user)
        paciente = get_object_or_404(Paciente, user=request.user)

        if paciente.contactos and nutriologo.id in paciente.contactos and paciente.id in nutriologo.contactos:
            paciente.contactos.remove(nutriologo.id)  #Se remueven ambos contactos
            nutriologo.contactos.remove(paciente.id)
            paciente.save()
            nutriologo.save()
            print(f"Contactos paciente {paciente.id} después de eliminar: ")
            print(paciente.contactos)
            print(f"Contactos nutriologo: {nutriologo.id} después de eliminar: ")
            print(nutriologo.contactos)

            # Respuesta JSON para confirmar el éxito
            return JsonResponse({"message": "Contacto eliminado exitosamente"})
        
        else:
            print("No hay contactos para eliminar")
            # Si el nutriologo no existe, devolvemos un mensaje de error
            return JsonResponse({"error": "No hay contactos para eliminar"})

        

    except Nutriologo.DoesNotExist:
        paciente = Paciente.objects.get(user=user)
        nutriologo = get_object_or_404(Nutriologo, user=request.user)

        if nutriologo.contactos and paciente.id in nutriologo.contactos and nutriologo.id in paciente.contactos:
            paciente.contactos.remove(nutriologo.id)  #Se remueven ambos contactos
            nutriologo.contactos.remove(paciente.id)
            paciente.save()
            nutriologo.save()
            print(f"Contactos paciente {paciente.id} después de eliminar: ")
            print(paciente.contactos)
            print(f"Contactos nutriologo: {nutriologo.id} después de eliminar: ")
            print(nutriologo.contactos)

            # Respuesta JSON para confirmar el éxito
            return JsonResponse({"message": "Contacto eliminado exitosamente"})
        
        else:
            print("No hay contactos para eliminar")
            # Si el nutriologo no existe, devolvemos un mensaje de error
            return JsonResponse({"error": "No hay contactos para eliminar"})
        
        return JsonResponse({"error": "El nutriologo no existe"})
    except Paciente.DoesNotExist:
        # Si el paciente no existe, devolvemos un mensaje de error
        return JsonResponse({"error": "El paciente no existe"})
    
def eliminar_solicitud(request, username):
    #La idea general es que obtenga al usuario actual (debe ser paciente) y al nutriologo que es el username de la URL
    user = get_object_or_404(User, username=username)
    nutriologo = get_object_or_404(Nutriologo, user=request.user)
    try:
        paciente = Paciente.objects.get(user=user)

        if not nutriologo.solicitudes:
            nutriologo.solicitudes = []
        if paciente.id in nutriologo.solicitudes:
            nutriologo.solicitudes.remove(paciente.id) #Se elimina la solicitud
        nutriologo.save()

        print(f"Contactos paciente {paciente.id}: ")
        print(paciente.contactos)
        print(f"Contactos nutriologo: {nutriologo.id}: ")
        print(nutriologo.contactos)
        nutriologo_user = nutriologo.user.username
        asunto = "Amistad"
        mensaje = f"{nutriologo_user} ha rechazado tu solicitud."
        url = reverse('ver_perfil', kwargs={'username': nutriologo})
        crear_notificacion(user,asunto,mensaje,url)

        # Respuesta JSON para confirmar el éxito
        return JsonResponse({"message": "Solicitud eliminada exitosamente"})

    except Nutriologo.DoesNotExist:
        # Si el nutriologo no existe, devolvemos un mensaje de error
        return JsonResponse({"error": "El nutriologo no existe"})
    except Paciente.DoesNotExist:
        # Si el paciente no existe, devolvemos un mensaje de error
        return JsonResponse({"error": "El paciente no existe"})



def perfilPublico(request, username,):
    # Obtener el usuario basado en el username
    user = get_object_or_404(User, username=username)
    
    # Intentar obtener el perfil de nutriologo para el usuario
    try:
        nutriologo = Nutriologo.objects.get(user=user)
        consultorio = Consultorio.objects.get(nutriologo=nutriologo)
        paciente = get_object_or_404(Paciente, user=request.user)
        especialidad = nutriologo.especialidad
        if nutriologo.foto_perfil:
            with nutriologo.foto_perfil.open('rb') as image_file:
                image_data = image_file.read()
                foto = base64.b64encode(image_data).decode('utf-8')
        else:
            foto = None
        if nutriologo.certificado:
            with nutriologo.certificado.open('rb') as pdf_file:
                pdf_data = pdf_file.read()
                certificado = base64.b64encode(pdf_data).decode('utf-8')
        else:
            certificado = None
        if nutriologo.curriculum:
            with nutriologo.curriculum.open('rb') as pdf_file:
                pdf_data = pdf_file.read()
                curriculum = base64.b64encode(pdf_data).decode('utf-8')
        else:
            curriculum = None

        #Verificar que los usuarios (Paciente y Nutriologo tienen una relacion)
        if not nutriologo.contactos:
            usuario_agregado = 0
        elif paciente.id in nutriologo.contactos:
            usuario_agregado = 1
        else:
            usuario_agregado = 0

        #Verificar que los los usuarios tienen una solicitud pendiente
        if not nutriologo.solicitudes:
            solicitud_pendiente = 0
        elif paciente.id in nutriologo.solicitudes:
            solicitud_pendiente = 1
        else:
            solicitud_pendiente = 0

        print(f"solicitud pendiente: {solicitud_pendiente}")

        datos = {
        'nombre': nutriologo.user.first_name,
        'apellidos' : nutriologo.user.last_name,
        'foto': foto,
        'correo': nutriologo.user.email,
        'telefono': nutriologo.telefono,
        'institucion': nutriologo.institucion_otorgamiento,
        'ubicacion': nutriologo.ubicacion,
        'especialidad' : codigoANombre(especialidad),
        'institucion': nutriologo.institucion_otorgamiento,
        'cedula': nutriologo.cedula,
        'descripcion' : nutriologo.descripcion,
        'direccion' : consultorio.direccion,
        'apertura' : consultorio.horario_apertura,
        'cierre' : consultorio.horario_cierre,
        'edad': nutriologo.edad,
        'sexo': nutriologo.sexo,
        'user': nutriologo.user.username,
        "nutriologo": 1,
        'facebook': nutriologo.enlace_facebook,
        'linkedin': nutriologo.enlace_linkedin,
        'instagram': nutriologo.enlace_instagram,
        'twitter':nutriologo.enlace_pagina_web,   
        'certificado':certificado,   
        'curriculum':curriculum, 
        'costo_consulta':consultorio.costo_consulta, 
        'usuario_agregado': usuario_agregado, 
        'solicitud_pendiente': solicitud_pendiente,
        'paciente': paciente,
    }
        return render(request, 'perfil_nutriologo.html', {'usuario': datos})
    
    except Nutriologo.DoesNotExist:
        try:
            paciente = Paciente.objects.get(user=user)
            nutriologo = get_object_or_404(Nutriologo, user=request.user)

            if paciente.foto_perfil:
                with paciente.foto_perfil.open('rb') as image_file:
                    image_data = image_file.read()
                    foto = base64.b64encode(image_data).decode('utf-8')
            else:
                foto = None

            #Verificar que los usuarios (Paciente y Nutriologo tienen una relacion)
            if not paciente.contactos:
                usuario_agregado = 0
            elif nutriologo.id in paciente.contactos:
                usuario_agregado = 1
            else:
                usuario_agregado = 0

            #Verificar que los los usuarios tienen una solicitud pendiente
            if not nutriologo.solicitudes:
                solicitud_pendiente = 0
            elif paciente.id in nutriologo.solicitudes:
                solicitud_pendiente = 1
            else:
                solicitud_pendiente = 0
            print(f"solicitud pendiente: {solicitud_pendiente}")
            datos = {
            'nombre': paciente.user.first_name,
            'apellidos' : paciente.user.last_name,
            'foto': foto,
            'correo': paciente.user.email,
            'telefono': paciente.telefono,
            'ubicacion': paciente.ubicacion,
            'edad': paciente.edad,
            'sexo': paciente.sexo,
            'user': paciente.user.username,
            "nutriologo": 0,
            'descripcion' : paciente.descripcion,
            'usuario_agregado': usuario_agregado,
            'solicitud_pendiente': solicitud_pendiente,
            #'facebook': nutriologo.enlace_facebook,
            #'linkedin': nutriologo.enlace_linkedin,
            #'instagram': nutriologo.enlace_instagram,
            #'twitter':nutriologo.enlace_pagina_web,    
            }
            return render(request, 'perfil_paciente_publico.html', {'usuario': datos})
        except Paciente.DoesNotExist:
            pass

@login_required
def datos(request):
    if request.user.groups.filter(name='Nutriologos').exists():
        return datos_nutriologo(request)
    elif request.user.groups.filter(name='Pacientes').exists():
        return datos_paciente(request)
    else:
        return datos_default(request)
    
def datos_default(request):
    usuario = "default"
    data ={
        'usuario':usuario,
    }
    return JsonResponse(data, safe=False)


def contacto_datos(request):
    if request.method == "POST":
        # Recoger los datos del formulario
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Guardar en la base de datos
        contacto = Contacto(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            message=message
        )
        contacto.save()

        # Enviar correo de confirmación al usuario
        enviar_correo(
            "Hemos recibido tu mensaje",
            email,
            "Gracias por ponerte en contacto con nosotros. Pronto nos pondremos en contacto contigo."
        )

        # Enviar correo al administrador
        enviar_correo(
            "Nuevo mensaje de contacto",
            settings.ADMIN_EMAIL,
            f"Has recibido un nuevo mensaje de {first_name} {last_name}.\n\nMensaje:\n{message}\n\nEmail: {email}\nTeléfono: {phone}"
        )

        # Mostrar un mensaje de éxito en la interfaz
        messages.success(request, "Gracias por ponerte en contacto con nosotros. Te responderemos pronto.")
    
    return render(request, 'home.html')