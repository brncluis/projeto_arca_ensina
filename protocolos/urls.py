from django.urls import path
from . import views

urlpatterns = [
    path('', views.protocolos_home, name='protocolos'),
    path('detalhes/', views.detalhes_do_protocolo, name='detalhes_do_protocolo'),
]