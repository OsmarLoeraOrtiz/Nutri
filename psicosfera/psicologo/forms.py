from django import forms
from .models import Psicologo,Consultorio


class FormPsicologo(forms.ModelForm):
    
    class Meta:
        model = Psicologo
        fields = '__all__'
        exclude = ['diario','user','contactos'] 
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'institucion_otorgamiento': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_obtencion': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'curriculum': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'certificado': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'identificacion_oficial': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'enlace_pagina_web': forms.URLInput(attrs={'class': 'form-control'}),
            'enlace_facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'enlace_instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'enlace_linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'fecha_registro': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'diario': forms.Textarea(attrs={'class': 'form-control'}), 
        }


class FormConsultorio(forms.ModelForm):
    
    class Meta:
        model = Consultorio
        fields = '__all__'
        exclude = ['psicologo']
        widgets = {
            'direccion': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'direccion-input'}
            ),
            'horario_apertura': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Formato HH:MM'}),
            'horario_cierre': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Formato HH:MM'}),
            'costo_consulta': forms.TextInput(attrs={'class': 'form-control', 'inputmode': 'numeric', 'pattern': '[0-9]*'}),
        }