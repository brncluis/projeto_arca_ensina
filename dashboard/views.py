from django.shortcuts import render
from .models import Paciente

def dashboard(request):
    return render(request, 'dashboard/index.html')

def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'dashboard/pacientes.html', {'pacientes': pacientes})