from django.views.generic import ListView, TemplateView
from django.http import JsonResponse
import googlemaps
from django.conf import settings
from nutriologo.models import Nutriologo, Consultorio
from nutriologo.especialidades import ESPECIALIDADES_CHOICES,ESPECIALIDADES_CHOICES_2
from django.db.models import F, Value, CharField
from django.shortcuts import render
from django.http import HttpResponse
from paciente.models import Paciente, Expediente
import base64

from evento.models import Evento, SolicitudAgenda
from .forms import FormPaciente
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from nutriologo.views import codigoANombre
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404



def datos_paciente(request):
    try:
        paciente_id = request.POST.get('paciente_id')
        paciente = Paciente.objects.get(id=paciente_id)
    except:
        paciente = Paciente.objects.get(user=request.user)

    nombre = paciente.user.first_name
    apellidos = str(paciente.user.last_name)
    correo_electronico = paciente.user.email
    descripcion = paciente.descripcion
    telefono = paciente.telefono
    ubicacion = paciente.ubicacion
    edad = paciente.edad
    sexo = paciente.sexo
    usuario = "registrado"
    notas_compartidas = ""
    if not paciente.contactos:
        contactos = None
    else:
        contactos = obtener_detalles_de_contactos(paciente.contactos)
    if paciente.foto_perfil:
        with paciente.foto_perfil.open('rb') as image_file:
            image_data = image_file.read()
            foto = base64.b64encode(image_data).decode('utf-8')
    else:
        foto = None
        
    try:
        expediente = Expediente.objects.get(paciente=paciente)
        notas_compartidas = expediente.notas_compartidas

    except:
        print("No hay expediente.")
    data ={
            'usuario':usuario,
            "foto": foto,
            "nombre" : nombre,
            "apellidos": apellidos,
            "correo" : correo_electronico,
            'descripcion': descripcion,
            "telefono" : telefono,
            "ubicacion" : ubicacion,
            "edad" : edad,
            "sexo" : sexo,
            "user": paciente.user.username,
            "nutriologo": 0,
            "notas_compartidas" : notas_compartidas,
            "contactos" : contactos,
        }
    return JsonResponse(data, safe=False)

def obtener_detalles_de_contactos(contactos):
    detalles_contactos = []
    if contactos:
        for contacto_id in contactos:
            try:
                nutriologo = Nutriologo.objects.get(id=contacto_id)
                detalles_contactos.append({
                    'nombre': nutriologo.user.first_name,
                    'apellido': nutriologo.user.last_name,
                    'especialidad': codigoANombre(nutriologo.especialidad),
                    'usuario': nutriologo.user.username,
                    'ubicacion': nutriologo.ubicacion,
                })
            except Nutriologo.DoesNotExist:
                # Manejar si el usuario no existe
                pass
    return detalles_contactos


@login_required
def actualizar_paciente(request):
    from home.views import crear_notificacion
    paciente = Paciente.objects.get(user=request.user)
    if request.method == 'POST':
        form = FormPaciente(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            try:
                # Guardar los cambios en el formulario pacienteForm
                paciente = form.save(commit=False)

                # Procesar los datos adicionales
                nombre = request.POST.get('firstName', '')  
                apellidos = request.POST.get('lastName', '')  
                correo = request.POST.get('correo2', '')  

                # Actualizar los campos adicionales en el modelo paciente
                paciente.user.first_name = nombre
                paciente.user.last_name = apellidos
                paciente.user.email = correo
                paciente.user.save()

                # Guardar los cambios en el modelo paciente
                paciente.save()
                perfil_url = reverse('perfil')
                message = "Cambios realizados correctamente."
                crear_notificacion(paciente.user,"Cambios", message, perfil_url)

            except Exception as e:
                messages.error(request, "Error al actualizar tus datos")
                return redirect('perfil')
            # Redirigir a la página de perfil con un indicador de éxito en la URL
            return redirect('actualizacion_exitosa')
        else:
            return HttpResponseRedirect(reverse('perfil') + '?error=true')
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

        

    
class PacienteInterfazView(TemplateView):
    template_name = 'interfaz-paciente.html'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
def autocompletar_especialidades(request):
    query = request.GET.get('query', '')
    
    # Realiza una consulta para obtener todos los objetos Nutriologos
    nutriologos = Nutriologo.objects.all()

    # Crea una lista de nombres completos a partir de los objetos Nutriologo
    nombres_completos_de_nutriologos = []

    for nutriologo in nutriologos:
        # Combina el primer nombre y el apellido
        nombre_completo = nombre_completo = f"{nutriologo.user.first_name} {nutriologo.user.last_name}"
        nombres_completos_de_nutriologos.append(nombre_completo)


    sugerencias_total = ESPECIALIDADES_CHOICES + nombres_completos_de_nutriologos

    # Filtrar las sugerencias que coinciden con la consulta del usuario
    sugerencias_filtradas = [s for s in sugerencias_total if query.lower() in s.lower()]

    # Devolver las sugerencias como un objeto JSON
    return JsonResponse(sugerencias_filtradas, safe=False)


def autocompletar_ubicaciones(request):
    query = request.GET.get('query', '')

    if query:
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        places = gmaps.places_autocomplete(input_text=query)

        suggestions = [place['description'] for place in places]

        return JsonResponse(suggestions, safe=False)

    return JsonResponse([], safe=False)
@login_required
def obtener_citas_paciente(request):
    paciente = Paciente.objects.get(user=request.user)
    citas = Evento.objects.filter(paciente=paciente)
    
    if citas:
        citasPaciente = []
        for cita in citas:                     
            citasPaciente.append({
                'id': cita.id,
                'id_nutriologo': cita.nutriologo.id,
                'nombre_nutriologo': cita.nutriologo.user.first_name + ' ' + cita.nutriologo.user.last_name,
                'title': cita.titulo,
                'start': cita.fecha_inicio.strftime('%Y-%m-%dT%H:%M:%S'),  # Formato ISO8601  
                'end': cita.fecha_fin.strftime('%Y-%m-%dT%H:%M:%S'), # Formato ISO8601 
                'fecha_inicio': cita.fecha_inicio.strftime('%Y-%m-%d'),   
                'fecha_fin': cita.fecha_fin.strftime('%Y-%m-%d'),# Formato ISO8601
                'hora_fin': cita.fecha_fin.strftime('%H:%M:%S'),  # Formato ISO8601
                'hora_inicio': cita.fecha_inicio.strftime('%H:%M:%S'),  # Formato ISO8601
            })
        return JsonResponse(citasPaciente, safe=False)

    return JsonResponse({'mensaje': 'Las citas no existe'}, status=404)

@login_required  
def obtener_solicitud_citas_enviadas_paciente(request):
    paciente = Paciente.objects.get(user=request.user)
    try:
        citas = SolicitudAgenda.objects.filter(paciente=paciente)
        if citas:
            citasPaciente = []
            for cita in citas:                     
                citasPaciente.append({
                    'id': cita.id,
                    'id_nutriologo': cita.nutriologo.id,
                    'nombre_nutriologo': cita.nutriologo.user.first_name + ' ' + cita.nutriologo.user.last_name,
                    'title': cita.titulo,
                    'start': cita.fecha_inicio.strftime('%Y-%m-%dT%H:%M:%S'),  # Formato ISO8601  
                    'end': cita.fecha_fin.strftime('%Y-%m-%dT%H:%M:%S'), # Formato ISO8601 
                    'fecha_inicio': cita.fecha_inicio.strftime('%Y-%m-%d'),   
                    'fecha_fin': cita.fecha_fin.strftime('%Y-%m-%d'),# Formato ISO8601
                    'hora_fin': cita.fecha_fin.strftime('%H:%M:%S'),  # Formato ISO8601
                    'hora_inicio': cita.fecha_inicio.strftime('%H:%M:%S'),  # Formato ISO8601
                    'motivo': cita.motivo
                })
            return JsonResponse(citasPaciente, safe=False)
        else:
            return JsonResponse({'mensaje': 'No hay citas para el nutriólogo y paciente dados.'}, status=404)

    except Nutriologo.DoesNotExist:
        return JsonResponse({'mensaje': 'Las citas no existe'}, status=404)  # El usuario no es un nutriólogo, continuar
    except Paciente.DoesNotExist:
        return JsonResponse({'mensaje': 'El paciente no existe'}, status=404)

#Este metodo filtrara los nutriologos por la especilidad ingresada o su nombre
def nutriologos_por_especialidad_nombre(request):
     lista_nombres = []

     if request.method == 'GET':
        inputText = request.GET.get('especialidad')

        #Primero verificamos si esta en la lista de especialidades
        if inputText in ESPECIALIDADES_CHOICES:
            # Obtén todos los objetos Nutriologo
            nutriologos = Nutriologo.objects.all()
            for nutriologo in nutriologos:
                especialidad = nutriologo.especialidad # Accede a la especialidad del nutriologo
                ubicacion = nutriologo.ubicacion # Accede a la especialidad del nutriologo
                ubicacion = ubicacion.replace(',', '-') # Accede a la especialidad del nutriologo
                if nutriologo.foto_perfil:
                    with nutriologo.foto_perfil.open('rb') as image_file:   #Obtiene la foto encriptada para mostrarla en la tarjeta
                        image_data = image_file.read()
                        foto = base64.b64encode(image_data).decode('utf-8')
                else:
                    foto = None
                for codigo, nombre in ESPECIALIDADES_CHOICES_2: #transforma el id en en nombre de la especialidad
                    if especialidad == codigo:
                        especialidad = nombre
                        break  # Terminamos el bucle cuando encontramos una coincidencia
                if especialidad == inputText: #verifica si la especialidad del usuario es la que se esta solicitando
                    #Ya que sabemos que tiene la esp solicitada, buscaremos su respectivo consultorio
                    consultorio = Consultorio.objects.get(nutriologo=nutriologo)
                    direccion_consultorio = consultorio.direccion
                    direccion_consultorio = direccion_consultorio.replace(',', '-')
                    costo_consulta = consultorio.costo_consulta
                    nombre_usuario = nutriologo.user.first_name + " "  +  nutriologo.user.last_name # Accede al nombre de usuario del usuario asociado al nutriólogo
                    username = nutriologo.user.username
                    lista_nombres.append((nombre_usuario,especialidad, direccion_consultorio, username, foto, costo_consulta, ubicacion))  # Agrega el nombre de usuario a la lista
            return JsonResponse(lista_nombres, safe=False)
        
        elif inputText not in ESPECIALIDADES_CHOICES:
            # Realiza una consulta para obtener todos los objetos Nutriologos
            nutriologos = Nutriologo.objects.all()
            for nutriologo in nutriologos:
                nombre = nutriologo.user.first_name + " "  +  nutriologo.user.last_name # Accede al nombre de usuario del usuario asociado al nutriólogo
                especialidad = nutriologo.especialidad # Accede a la especialidad del nutriologo
                ubicacion = nutriologo.ubicacion # Accede a la especialidad del nutriologo
                ubicacion = ubicacion.replace(',', '-') # Accede a la especialidad del nutriologo
                if nutriologo.foto_perfil:
                    with nutriologo.foto_perfil.open('rb') as image_file:   #Obtiene la foto encriptada para mostrarla en la tarjeta
                        image_data = image_file.read()
                        foto = base64.b64encode(image_data).decode('utf-8')
                else:
                    foto = None
                for codigo, esp in ESPECIALIDADES_CHOICES_2: #transforma el id en en nombre de la especialidad
                    if especialidad == codigo:
                        especialidad = esp
                        break  # Terminamos el bucle cuando encontramos una coincidencia
                if nombre ==  inputText:
                    #Ya que sabemos que tiene la esp solicitada, buscaremos su respectivo consultorio
                    consultorio = Consultorio.objects.get(nutriologo=nutriologo)
                    direccion_consultorio = consultorio.direccion
                    direccion_consultorio = direccion_consultorio.replace(',', '-')
                    costo_consulta = consultorio.costo_consulta
                    username = nutriologo.user.username
                    lista_nombres.append((nombre,especialidad,direccion_consultorio, username, foto, costo_consulta, ubicacion))  # Agrega el nombre de usuario a la lista
            return JsonResponse(lista_nombres, safe=False)
        
        else:
            #Si no cumple nada de esto regresa una lista vacia
            return JsonResponse(lista_nombres, safe=False)
        # Devolver las sugerencias como un objeto JSON
    


   




    
      
 