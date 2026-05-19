from django.contrib import admin
from .models import Protocolo, Sintoma, Categoria, Medicamento


admin.site.register(Protocolo)
admin.site.register(Sintoma)
admin.site.register(Categoria)
admin.site.register(Medicamento)