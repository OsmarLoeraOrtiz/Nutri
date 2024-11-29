from nutriologo.especialidades import ESPECIALIDADES_CHOICES_2
from .models import Consultorio, Nutriologo
from evento.models import Evento, SolicitudAgenda
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from paciente.models import Expediente, Paciente
from django.http import  JsonResponse
import base64
from django.http import HttpResponse
from .forms import FormNutriologo, FormConsultorio 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User



@login_required
def interfaz_nutriologo(request):
    nutriologo = Nutriologo.objects.get(user=request.user)
    data = {}
    if nutriologo.diario:
        data = {
            'diario': nutriologo.diario
        }
    
    return render(request, 'mi_consultorio.html',data)

@login_required
def guardar_cita(request):
    if request.method == 'POST':
        nutriologo = Nutriologo.objects.get(user=request.user)
        try:
            paciente = User.objects.get(username=request.POST.get('paciente'))
            paciente = Paciente.objects.get(user=paciente)
        except:
            return JsonResponse({'mensaje': 'Nombre de usuario del paciente invalido'})
            
        titulo = request.POST.get('titulo')
        fecha_inicio = request.POST.get('start').replace('-06:00',"")
        fecha_fin = request.POST.get('end').replace('-06:00',"")
        cita = Evento(paciente=paciente,nutriologo=nutriologo,titulo=titulo, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        cita.save()
        
        return JsonResponse({'mensaje': 'Cita guardado con éxito'})
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)  
    
@login_required
def eliminar_cita(request):
    if request.method == 'POST':
        try:
            cita = Evento.objects.get(id=request.POST.get('id'))
            cita.delete()
            return JsonResponse({'mensaje': 'Cita eliminada con éxito'})
        except Evento.DoesNotExist:
            return JsonResponse({'mensaje': 'La cita no existe'}, status=404)
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)
    
@login_required
def eliminar_solicitud_cita(request):
    if request.method == 'POST':
        try:
            cita = SolicitudAgenda.objects.get(id=request.POST.get('id'))
            cita.delete()
            return JsonResponse({'mensaje': 'Cita eliminada con éxito'})
        except Evento.DoesNotExist:
            return JsonResponse({'mensaje': 'La cita no existe'}, status=404)
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)
       
 
@login_required
def obtener_citas(request):
    nutriologo = Nutriologo.objects.get(user=request.user)
    citas = Evento.objects.filter(nutriologo=nutriologo)
    
    if citas:
        citasNutriologo = []
        for cita in citas:                     
            citasNutriologo.append({
                'id': cita.id,
                'id_paciente': cita.paciente.id,
                'nombre_paciente': cita.paciente.user.first_name + ' ' + cita.paciente.user.last_name,
                'title': cita.titulo,
                'start': cita.fecha_inicio.strftime('%Y-%m-%dT%H:%M:%S'),  # Formato ISO8601  
                'end': cita.fecha_fin.strftime('%Y-%m-%dT%H:%M:%S'), # Formato ISO8601 
                'fecha_inicio': cita.fecha_inicio.strftime('%Y-%m-%d'),   
                'fecha_fin': cita.fecha_fin.strftime('%Y-%m-%d'),# Formato ISO8601
                'hora_fin': cita.fecha_fin.strftime('%H:%M:%S'),  # Formato ISO8601
                'hora_inicio': cita.fecha_inicio.strftime('%H:%M:%S'),  # Formato ISO8601
            })
        return JsonResponse(citasNutriologo, safe=False)

    return JsonResponse({'mensaje': 'Las citas no existe'}, status=404)



@login_required
def obtener_solicitud_citas(request):
    nutriologo = Nutriologo.objects.get(user=request.user)
    citas = SolicitudAgenda.objects.filter(nutriologo=nutriologo)
    
    if citas:
        citasNutriologo = []
        for cita in citas:                     
            citasNutriologo.append({
                'id': cita.id,
                'id_paciente': cita.paciente.id,
                'nombre_paciente': cita.paciente.user.first_name + ' ' + cita.paciente.user.last_name,
                'title': cita.titulo,
                'start': cita.fecha_inicio.strftime('%Y-%m-%dT%H:%M:%S'),  # Formato ISO8601  
                'end': cita.fecha_fin.strftime('%Y-%m-%dT%H:%M:%S'), # Formato ISO8601 
                'fecha_inicio': cita.fecha_inicio.strftime('%Y-%m-%d'),   
                'fecha_fin': cita.fecha_fin.strftime('%Y-%m-%d'),# Formato ISO8601
                'hora_fin': cita.fecha_fin.strftime('%H:%M:%S'),  # Formato ISO8601
                'hora_inicio': cita.fecha_inicio.strftime('%H:%M:%S'),  # Formato ISO8601
                'motivo': cita.motivo
            })
        return JsonResponse(citasNutriologo, safe=False)

    return JsonResponse({'mensaje': 'Las citas no existe'}, status=404)



@login_required
def obtener_citas_publico(request, username):
     # Obtener el usuario basado en el username
    user = get_object_or_404(User, username=username)
    # Intentar obtener el perfil de nutriologo para el usuario
    try:
        nutriologo = Nutriologo.objects.get(user=user)
        citas = Evento.objects.filter(nutriologo=nutriologo)
        citasNutriologo = []
        for cita in citas:
            citasNutriologo.append({
                'id': cita.id,
                'id_paciente': cita.paciente.id,
                'nombre_paciente': cita.paciente.user.first_name + ' ' + cita.paciente.user.last_name,
                'title': cita.titulo,
                'start': cita.fecha_inicio.strftime('%Y-%m-%dT%H:%M:%S'),  # Formato ISO8601  
                'end': cita.fecha_fin.strftime('%Y-%m-%dT%H:%M:%S'), # Formato ISO8601 
                'fecha_inicio': cita.fecha_inicio.strftime('%Y-%m-%d'),   
                'fecha_fin': cita.fecha_fin.strftime('%Y-%m-%d'),# Formato ISO8601
                'hora_fin': cita.fecha_fin.strftime('%H:%M:%S'),  # Formato ISO8601
                'hora_inicio': cita.fecha_inicio.strftime('%H:%M:%S'),  # Formato ISO8601
            })

        return JsonResponse(citasNutriologo, safe=False)
    except Nutriologo.DoesNotExist:
        return JsonResponse({'mensaje': 'Las citas no existe'}, status=404)  # El usuario no es un nutriólogo, continuar

@login_required  
def obtener_solicitud_citas_enviadas_nutriologo(request,username):
    paciente = Paciente.objects.get(user=request.user)
    user = get_object_or_404(User, username=username)
    try:
        nutriologo = Nutriologo.objects.get(user=user)
        citas = SolicitudAgenda.objects.filter(paciente=paciente, nutriologo=nutriologo)
        if citas:
            citasPaciente = []
            for cita in citas:                     
                citasPaciente.append({
                    'id': cita.id,
                    'id_paciente': cita.paciente.id,
                    'nombre_paciente': cita.paciente.user.first_name + ' ' + cita.paciente.user.last_name,
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
            return JsonResponse({'mensaje': 'No hay citas para el nutriologo y paciente dados.'}, status=404)

    except Nutriologo.DoesNotExist:
        return JsonResponse({'mensaje': 'Las citas no existe'}, status=404)  # El usuario no es un nutriologo, continuar
    except Paciente.DoesNotExist:
        return JsonResponse({'mensaje': 'El paciente no existe'}, status=404)
    
@login_required  
def obtener_solicitud_citas_enviadas(request):
    paciente = Paciente.objects.get(user=request.user)
    try:
        citas = SolicitudAgenda.objects.filter(paciente=paciente)
        if citas:
            citasPaciente = []
            for cita in citas:                     
                citasPaciente.append({
                    'id': cita.id,
                    'id_paciente': cita.paciente.id,
                    'nombre_paciente': cita.paciente.user.first_name + ' ' + cita.paciente.user.last_name,
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
            return JsonResponse({'mensaje': 'No hay citas para el nutriologo y paciente dados.'}, status=404)

    except Nutriologo.DoesNotExist:
        return JsonResponse({'mensaje': 'Las citas no existe'}, status=404)  # El usuario no es un nutriologo, continuar
    except Paciente.DoesNotExist:
        return JsonResponse({'mensaje': 'El paciente no existe'}, status=404)

@login_required
def datos_nutriologo(request):
    nutriologo = Nutriologo.objects.get(user=request.user)
    nutriologo_id = nutriologo.id
    usuario = "registrado"
    especialidad = nutriologo.especialidad
    direccion = ""
    apertura = ""
    cierre = ""
    if not nutriologo.contactos:
        contactos = None
    else:
        contactos = obtener_detalles_de_contactos(nutriologo.contactos)
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

    try:
        consultorio = Consultorio.objects.get(nutriologo=nutriologo_id)
        direccion = consultorio.direccion
        apertura = consultorio.horario_apertura
        cierre = consultorio.horario_cierre
        costo_consulta = consultorio.costo_consulta
    except:
        pass
    datos = {
        'usuario':usuario,
        'cons_registrado': 0,
        'foto': foto,
        'nombre': nutriologo.user.first_name,
        'apellidos': nutriologo.user.last_name,
        'correo': nutriologo.user.email,
        'telefono': nutriologo.telefono,
        'descripcion': nutriologo.descripcion,
        'ubicacion': nutriologo.ubicacion,
        'especialidad' : codigoANombre(especialidad),
        'institucion' : nutriologo.institucion_otorgamiento,
        'cedula' : nutriologo.cedula,
        'certificado': certificado,
        'curriculum' : curriculum,
        'edad': nutriologo.edad,
        'sexo': nutriologo.sexo,
        'user': nutriologo.user.username,
        "nutriologo": 1,
        'facebook': nutriologo.enlace_facebook,
        'linkedin': nutriologo.enlace_linkedin,
        'instagram': nutriologo.enlace_instagram,
        'twitter':nutriologo.enlace_pagina_web,   
        'diario': nutriologo.diario,
        'direccion': direccion,
        'apertura': apertura,
        'cierre': cierre,
        'costo_consulta': costo_consulta,
        "contactos" : contactos,
    }
    
    return JsonResponse(datos, safe=False)

   
def obtener_detalles_de_contactos(contactos):
    detalles_contactos = []
    if contactos:
        for contacto_id in contactos:
            try:
                paciente = Paciente.objects.get(id=contacto_id)
                detalles_contactos.append({
                    'nombre': paciente.user.first_name,
                    'apellido': paciente.user.last_name,
                    'usuario': paciente.user.username,
                    'ubicacion': paciente.ubicacion,
                })
            except Nutriologo.DoesNotExist:
                # Manejar si el usuario no existe
                pass
    print(detalles_contactos)
    return detalles_contactos

def codigoANombre(especialidad):
    for codigo, nombre in ESPECIALIDADES_CHOICES_2: #transforma el id en el nombre de la especialidad
    	if especialidad == codigo:
            return nombre

@login_required
def diario_nutriologo(request):
    nutriologo = Nutriologo.objects.get(user=request.user)
    if nutriologo.diario:
        return JsonResponse({'diario':nutriologo.diario})

@login_required
def actualizar_nutriologo(request):
    from home.views import crear_notificacion
    if request.method == 'POST':
        nutriologo = Nutriologo.objects.get(user=request.user)
        form = FormNutriologo(request.POST, request.FILES, instance=nutriologo)
        if form.is_valid():
            try:
                # Guardar los cambios en el formulario NutriologoForm
                nutriologo = form.save(commit=False)

                # Procesar los datos adicionales
                nombre = request.POST.get('firstName', '') 
                apellidos = request.POST.get('lastName', '')  
                correo = request.POST.get('correo2', '')  

                # Actualizar los campos adicionales en el modelo nutriologo
                nutriologo.user.first_name = nombre
                nutriologo.user.last_name = apellidos
                nutriologo.user.email = correo
                nutriologo.user.save()

                # Guardar los cambios en el modelo nutriologo
                nutriologo.save()
                perfil_url = reverse('perfil')
                message = "Cambios realizados correctamente en tus datos personales."
                crear_notificacion(nutriologo.user,"Cambios", message, perfil_url)
            except Exception as e:
                messages.error(request, "Error al actualizar tus datos")
                return redirect('perfil')
            # Redirigir a la página de perfil con un indicador de éxito en la URL
            return redirect('perfil')
        else:
            return HttpResponseRedirect(reverse('perfil') + '?error=true')
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

@login_required
def actualizar_consultorio(request):
    from home.views import crear_notificacion
    if request.method == 'POST':
        nutriologo = Nutriologo.objects.get(user=request.user)
        consultorio = Consultorio.objects.get(nutriologo=nutriologo)
        form = FormConsultorio(request.POST, instance=consultorio)
        if form.is_valid():
            consultorio = form.save()
            perfil_url = reverse('perfil')
            message = "Cambios realizados correctamente en el consultorio."
            crear_notificacion(nutriologo.user,"Cambios", message, perfil_url)
            return redirect('perfil')
        else:
            messages.error(request, "Datos invalidos.")
            return redirect('perfil')
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)    



def guardar_notas(request):
    if request.method == 'POST':
        paciente_id = request.POST.get('id', '') 
        contenido = request.POST.get('contenidoCompartidas', '')  
        paciente = Paciente.objects.get(id=paciente_id)
        try:
            expediente = Expediente.objects.get(paciente=paciente)
            expediente.notas_compartidas = contenido
        except:
            usuario = request.user
            nutriologo = usuario.nutriologo
            expediente = Expediente(paciente=paciente,nutriologo=nutriologo, notas_compartidas=contenido)
        
        expediente.save()
    
        
        return JsonResponse({'mensaje': 'Expediente guardado con éxito'})
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)



def guardar_diario(request):
    if request.method == 'POST':
        notas= request.POST.get('contenido', None)
        nutriologo = Nutriologo.objects.get(user=request.user)
        nutriologo.diario = notas
        nutriologo.save()
        
        return JsonResponse({'mensaje': 'Expediente guardado con éxito'})
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

def obtener_pacientes(request):
    # Obtener una instancia de MiModelo (puedes ajustar esto según tus necesidades)
    nutriologo = Nutriologo.objects.get(user=request.user)
    contactos = nutriologo.contactos
    detalles_contactos = []
    contactos = {'3':3}
    if contactos:
        for contacto_id in contactos:
            try:
                paciente = Paciente.objects.get(id=contacto_id)
                detalles_contactos.append({
                    'usuario': paciente.user.username,
                })
            except Nutriologo.DoesNotExist:
                pass
    print(detalles_contactos)
    data = {'pacientes': detalles_contactos}

    return JsonResponse(data, safe=False)




def paciente_pdf(request,paciente_id):
    if paciente_id:
        paciente = Paciente.objects.get(id=paciente_id)
        nombre = str(paciente.user.last_name) + " " + str(paciente.user.first_name)
        correo_electronico = paciente.user.email
        telefono = paciente.telefono
        edad = paciente.edad
        sexo = paciente.sexo
        foto = None

        if paciente.foto_perfil:
            with paciente.foto_perfil.open('rb') as image_file:
                image_data = image_file.read()
                foto = base64.b64encode(image_data).decode('utf-8')

        # Crear una respuesta HTTP con el contenido del PDF
        buffer = BytesIO()

        # Crear el objeto PDF
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        # Lista para contener los elementos del PDF
        elements = []

        # Estilos para el formato de texto
        styles = getSampleStyleSheet()
        titulo_style = styles["Title"]
        normal_style = styles["Normal"]

        # Añadir la imagen (foto) junto al nombre
        if foto:
            image = Image(BytesIO(base64.b64decode(foto)))
            image.drawHeight = 100
            image.drawWidth = 100

            # Crear un párrafo que contiene la imagen y el nombre
            foto_nombre_paragraph = Paragraph('<br/><br/><br/><br/><br/><br/>', normal_style)  # Añade espacio en blanco
            foto_nombre_paragraph.add(image)
            foto_nombre_paragraph.add(Spacer(1, 5))  # Espacio entre la imagen y el nombre
            foto_nombre_paragraph.add(nombre)

            elements.append(foto_nombre_paragraph)
        else:
            # Si no hay imagen, solo agrega el nombre
            elements.append(Paragraph(nombre, titulo_style))

        # Agregar otros datos con letra más pequeña
        datos = [
            "Correo Electrónico: {}".format(correo_electronico),
            "Teléfono: {}".format(telefono),
            "Edad: {}".format(edad),
            "Sexo: {}".format(sexo),
        ]

        for dato in datos:
            elements.append(Spacer(1, 12))  # Espacio entre los datos
            elements.append(Paragraph(dato, normal_style))

        # Construir el PDF
        doc.build(elements)

        # Obtener el contenido del PDF desde el búfer y cerrar el búfer
        pdf = buffer.getvalue()
        buffer.close()

        # Configurar la respuesta HTTP
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mi_pdf.pdf"'

        # Escribir el contenido del PDF en la respuesta HTTP
        response.write(pdf)

        return response
    return JsonResponse({'mensaje': 'Selecciona a un paciente'}, status=405)