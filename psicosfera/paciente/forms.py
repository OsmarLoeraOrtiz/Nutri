from django import forms
from .models import Paciente, SEXO_CHOICES


class FormPaciente(forms.ModelForm):
    
    class Meta:
        model = Paciente
        fields = '__all__'
        exclude = ['user','contactos','correo_verificado']
        
        widgets = {
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'direccion-input'}
            ),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control'}),
            
            
        }
