from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True,label=("Nombre(s)"),)
    last_name = forms.CharField(max_length=30, required=True,label=("Apellido(s)"))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class ReestablecerContraseñaForm(forms.Form):
    password1 = forms.CharField(
        label=("Contraseña"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
    )
    password2 = forms.CharField(
        label=("Confirmar contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=("Para verificar, introduzca la misma contraseña que introdujo antes."),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError(("La dirección de correo electrónico que ingresaste no pertenece a ningún usuario."))
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(("Los dos campos de contraseña no coinciden"))
        return cleaned_data
    
    