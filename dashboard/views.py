from django.shortcuts import render
from .models import Paciente, Consulta

def dashboard(request):
    pacientes = Paciente.objects.all()
    return render(request, 'dashboard/index.html', {'pacientes': pacientes})

def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'dashboard/pacientes.html', {'pacientes': pacientes})

def historico_paciente(request, id):
    paciente = Paciente.objects.get(id=id)
    consulta_paciente = Consulta.objects.filter(paciente=paciente)
    return render(request, 'dashboard/historico.html', {'paciente': paciente, 'consultas': consulta_paciente})