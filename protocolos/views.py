from django.shortcuts import render

def protocolos_home(request):
    return render(request, 'protocolos/index.html')


def detalhes_protocolo(request):
    return render(request, 'protocolos/detalhes.html')


def filtrar_sintomas(request):
    return render(request, 'protocolos/filtrar_sintomas.html')