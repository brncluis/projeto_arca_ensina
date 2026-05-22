from django.urls import path
from . import views

urlpatterns = [
    path('', views.protocolos_home, name='protocolos'),
    path('detalhes/', views.detalhes_protocolo, name='detalhes_do_protocolo'),
    path('fluxograma/', views.fluxograma, name='fluxograma'),
    path('detalhes_sedacao/', views.detalhes_protocolo_sedacao, name='detalhes_sedacao'),
    path('fluxograma_sedacao/', views.fluxograma_sedacao, name='fluxograma_sedacao'),
    path('calculadora/', views.calculadora_dosagens, name='calculadora_dosagens'),
]

