from django.contrib import admin
from .models import Paciente, Consulta, Medico, PacienteExportado

admin.site.register(Paciente)
admin.site.register(Consulta)

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'crm', 'especialidade')
    search_fields = ('nome', 'crm')
 
 
@admin.register(PacienteExportado)
class PacienteExportadoAdmin(admin.ModelAdmin):
    list_display   = ('paciente', 'medico_destino', 'exportado_por', 'data_exportacao')
    list_filter    = ('medico_destino', 'exportado_por', 'data_exportacao')
    search_fields  = ('paciente__nome', 'medico_destino__nome', 'exportado_por__username')
    readonly_fields = ('data_exportacao',)
    date_hierarchy  = 'data_exportacao'