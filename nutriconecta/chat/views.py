from django.shortcuts import render
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.contrib.auth.models import User
from paciente.models import Paciente
from nutriologo.models import Nutriologo


from typing import List, Union

class UsersListView(LoginRequiredMixin, ListView):
    http_method_names = ['get', ]

    def get_queryset(self):
        user = self.request.user
        try:
            nutriologo = Nutriologo.objects.get(user=user)
            print("es nutriologo")
            print(nutriologo.contactos)
            if not nutriologo.contactos:
                nutriologo.contactos = []
            
            return nutriologo.contactos

        except Nutriologo.DoesNotExist:
            pass
        
        try:
            paciente = Paciente.objects.get(user=user)
            print("es paciente")
            print(paciente.contactos)
            if not paciente.contactos:
                paciente.contactos = []
            
            return paciente.contactos

        except Paciente.DoesNotExist:
            pass
    


    def render_to_response(self, context, **response_kwargs):
        # Obtener la lista de IDs de contactos
        contactos_ids = context['object_list']
        print(contactos_ids)

        # Crear una lista de diccionarios con información de cada contacto
        data = []

        for contacto_id in contactos_ids:
            try:
                contacto = Nutriologo.objects.get(id=contacto_id)
                usuario = contacto.user
            except Nutriologo.DoesNotExist:
                # Si no es Nutriologo, intentar obtenerlo como Paciente
                try:
                    contacto = Paciente.objects.get(id=contacto_id)
                    usuario = contacto.user
                except Paciente.DoesNotExist:
                    # Manejar el caso en que no se encontró ni Nutriologo ni Paciente
                    print(f"No se encontró ningún usuario con ID {contacto_id}")
                    continue
            
            # Agregar detalles relevantes al diccionario
            data.append({
                "username": usuario.username,
                "pk": str(usuario.pk),
                # Agrega más campos según sea necesario
            })

        return JsonResponse(data, safe=False, **response_kwargs)
