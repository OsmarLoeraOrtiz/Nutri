from django.contrib import admin
from .models import Paciente, Expediente

# Register your models here.
admin.site.register(Paciente)
admin.site.register(Expediente)
