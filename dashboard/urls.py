from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pacientes/', views.lista_pacientes, name='pacientes'),
    path('pacientes/<int:id>/', views.historico_paciente, name='historico_paciente'),
    path('cadastrar/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('prontuario/<int:id>/', views.prontuario_paciente, name='prontuario_paciente'),
]