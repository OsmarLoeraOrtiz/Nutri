from datetime import datetime
import os
from django.templatetags.static import static
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import *
from django.core.files.base import ContentFile

from django.views.generic import TemplateView

from django.contrib.auth.models import User, Group, Permission
from psicologo.models import Psicologo
from paciente.models import Paciente
from psicologo.forms import FormPsicologo, FormConsultorio
from paciente.forms import FormPaciente
from django.db.models.signals import post_save


# @login_required
# def agregar_paciente(request):
#     if not request.user.groups.filter(name='Pacientes').exists():
#         paciente_group = Group.objects.get(name='Pacientes')
#         request.user.groups.add(paciente_group)
#     return redirect('nuevo_paciente')  

# @login_required
# def agregar_psicologo(request):
#     print(request)
#     if not request.user.groups.filter(name='Psicologos').exists():
#         psicologo_group = Group.objects.get(name='Psicologos')
#         request.user.groups.add(psicologo_group)
#     return redirect('nuevo_psicologo') 

# @login_required
# def usuario_registrado(request):
#     if not request.user.groups.filter(name='Usuario-Registrado').exists():
#         usuario_registrado_group = Group.objects.get(name='Usuario-Registrado')
#         request.user.groups.add(usuario_registrado_group)
#     return redirect('home') 

class NuevoPsicologo(View):
    def get(self, request):
        form = FormPsicologo(initial={'user': self.request.user})
        print(form)
        return render(request, 'psicologo/psicologo_form.html', {'form': form})
    def post(self, request):
        form = FormPsicologo(request.POST, request.FILES)
        print(request.POST)
        print(self.request.user)
  
        if form.is_valid():
            nuevo_grupo, creado = Group.objects.get_or_create(name='Psicologos')
            # if creado:
            #     permiso = Permission.objects.get(codename='change_blogpost')  
            #     nuevo_grupo.permissions.add(permiso)        
            usuario = User.objects.get(username=self.request.user)
            usuario.groups.add(nuevo_grupo)    
            #form.save()
            #return redirect('nuevo-consultorio')
            nuevo_psicologo = form.save(commit=False)  # No guardes inmediatamente en la base de datos
            # Verificar si se cargó una imagen en el formulario
            if 'foto_perfil' in request.FILES:
                nuevo_psicologo.foto_perfil = request.FILES['foto_perfil']

            if 'foto_perfil' not in request.FILES:
                ruta_imagen_por_defecto = os.path.join(settings.BASE_DIR, 'static', 'img', 'usuario.png')
                with open(ruta_imagen_por_defecto, 'rb') as imagen_por_defecto:
                    nuevo_psicologo.foto_perfil.save('usuario.png', ContentFile(imagen_por_defecto.read()), save=True)

            # Verificar si se cargó una identificación en el formulario
            if 'identificacion' in request.FILES:
                nuevo_psicologo.identificacion_oficial = request.FILES['identificacion']

            # Verificar si se cargó un curriculum en el formulario
            if 'curriculum' in request.FILES:
                nuevo_psicologo.curriculum = request.FILES['curriculum']

            # Verificar si se cargó un certificado en el formulario
            if 'certificado' in request.FILES:
                nuevo_psicologo.certificado = request.FILES['certificado']
            
            nuevo_psicologo.user = request.user  # Asumiendo que el usuario está autenticado
            nuevo_psicologo.save()
            return redirect('nuevo-consultorio')

        else:
            # No necesitas iterar sobre form.error_messages
            for field, errors in form.errors.items():
                message = f"{field.capitalize()}: {errors[0]}"  # Obtén el primer error
                messages.error(request, message)
                print(message)
            error_message = "Información incorrecta. Corrige tus datos e intenta de nuevo." 
            return render(request, 'psicologo/psicologo_form.html', {'form': form, 'error_message': error_message})
        
class NuevoConsultorio(View):
    def get(self, request):
        psicologo = Psicologo.objects.get(user=self.request.user)
        psicologo_id = psicologo.id
        print(psicologo_id)
        form = FormConsultorio(initial={'psicologo': psicologo_id})
        return render(request, 'consultorio/consultorio_form.html', {'form': form})
    def post(self, request):
        form = FormConsultorio(request.POST)
        print(request.POST)
        print(self.request.user)
 
        if form.is_valid():

            nuevo_grupo, creado = Group.objects.get_or_create(name='Consultorios')
            psicologo_actual = Psicologo.objects.get(user=self.request.user)
            usuario = User.objects.get(username=self.request.user)
            usuario.groups.add(nuevo_grupo)

            nuevo_consultorio = form.save(commit=False)
            nuevo_consultorio.psicologo = psicologo_actual
            nuevo_consultorio.save()

            return redirect('home')
        else:
            # No necesitas iterar sobre form.error_messages
            for field, errors in form.errors.items():
                message = f"{field.capitalize()}: {errors[0]}"  # Obtén el primer error
                messages.error(request, message)
                print(message)
                print("ERROR")
                print(form)
            return render(request, 'consultorio/consultorio_form.html', {'form': form})

class NuevoPaciente(CreateView):
    def get(self, request):
        form = FormPaciente(initial={'user': self.request.user})
        print(form)
        return render(request, 'paciente/paciente_form.html', {'form': form})
    def post(self, request):
        form = FormPaciente(request.POST, request.FILES)
        print(request.POST)
        print(self.request.user)

        if form.is_valid():
            nuevo_grupo, creado = Group.objects.get_or_create(name='Pacientes')
            # if creado:
            #     permiso = Permission.objects.get(codename='change_blogpost')  
            #     nuevo_grupo.permissions.add(permiso)        
            usuario = User.objects.get(username=self.request.user)
            usuario.groups.add(nuevo_grupo)    
            #form.save()
            #return redirect('home')
            nuevo_paciente = form.save(commit=False)  # No guardes inmediatamente en la base de datos
            # Verificar si se cargó una imagen en el formulario
            if 'foto_perfil' in request.FILES:
                nuevo_paciente.foto_perfil = request.FILES['foto_perfil']

            if 'foto_perfil' not in request.FILES:
                ruta_imagen_por_defecto = os.path.join(settings.BASE_DIR, 'static', 'img', 'usuario.png')
                with open(ruta_imagen_por_defecto, 'rb') as imagen_por_defecto:
                    nuevo_paciente.foto_perfil.save('usuario.png', ContentFile(imagen_por_defecto.read()), save=True)

            nuevo_paciente.user = request.user  # Asumiendo que el usuario está autenticado
            nuevo_paciente.save()
            return redirect('home')
        
        else:
            # No necesitas iterar sobre form.error_messages
            for field, errors in form.errors.items():
                message = f"{field.capitalize()}: {errors[0]}"  # Obtén el primer error
                messages.error(request, message, extra_tags='form_error')
            error_message = "Información incorrecta. Corrige tus datos e intenta de nuevo."    
            return render(request, 'paciente/paciente_form.html', {'form': form, 'error_message': error_message})


class VRegistro(View):
    def get(self, request):
        form = RegistroForm()
        form.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        form.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        form.fields['password2'].widget.attrs['placeholder'] = 'Confirmar contraseña'
        form.fields['first_name'].widget.attrs['placeholder'] = 'Nombre(s)'
        form.fields['last_name'].widget.attrs['placeholder'] = 'Apellido(s)'
        form.fields['email'].widget.attrs['placeholder'] = 'Correo Electrónico'

        form.fields['username'].widget.attrs['class'] = 'form-control form-control-user'
        form.fields['password1'].widget.attrs['class'] = 'form-control form-control-user'
        form.fields['password2'].widget.attrs['class'] = 'form-control form-control-user'
        form.fields['first_name'].widget.attrs['class'] = 'form-control form-control-user'
        form.fields['last_name'].widget.attrs['class'] = 'form-control form-control-user'
        form.fields['email'].widget.attrs['class'] = 'form-control form-control-user'
        return render(request, "registro/registro.html",{'form':form})

    def post(self, request):
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('registro-usuario')
        else:
            # No necesitas iterar sobre form.error_messages
            for field, errors in form.errors.items():
                message = f"{field.capitalize()}: {errors[0]}"  # Obtén el primer error
                messages.error(request, message, extra_tags='registro_error')
            return render(request, "registro/registro.html", {'form': form})
        

class RegistroUsuarioView(TemplateView):
    template_name = 'registro/registroUsuario.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Usuario-Registrado').exists():
            return redirect('home')  # Ajusta 'home' a la URL correcta
        else:
            return super().dispatch(request, *args, **kwargs)
    
def calcular_edad(request):
    fecha_nacimiento_str = request.GET.get('fecha_nacimiento')
    fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
    
    hoy = datetime.now().date()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    
    return JsonResponse({'edad': edad})
 
def loguear(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contraseña = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre_usuario, password=contraseña)
            if usuario is not None:
                login(request, usuario)
                return redirect('home')
            else:
                messages.error(request, "Usuario no válido.",  extra_tags='login_error')  # Agrega este mensaje de error con etiqueta 'error'
        else:
            messages.error(request, "Contraseña o Usuario inválidos.",  extra_tags='login_error')  # Agrega este mensaje de error con etiqueta 'error'
    else:
        form = AuthenticationForm()
        form.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        form.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
        form.fields['username'].widget.attrs['class'] = 'form-control form-control-user'
        form.fields['password'].widget.attrs['class'] = 'form-control form-control-user'
    return render(request, "login/login.html", {'form': form})
        
def cerrarSesion(request):
    logout(request)
    return redirect('home')
    
def reestablecer_contraseña(request):
    if request.method=="POST":
            form = ReestablecerContraseñaForm(request.POST)
            if form.is_valid():
                correo = form.cleaned_data.get("email")
                usuario = authenticate(email=correo)
                if usuario is not None:
                    nuevaContraseña = form.cleaned_data.get("password1")
                    usuario.set_password(nuevaContraseña)
                    usuario.save()                                        #No reestablece la contraseña
                    return redirect('iniciar_sesion')
                else:
                    return redirect('iniciar_sesion')
                    #messages.error(request, "Correo no existente")
    else:  
            form = ReestablecerContraseñaForm()
    return render(request, "registro/reestablecer.html",{'form':form})


    
    
    
    
