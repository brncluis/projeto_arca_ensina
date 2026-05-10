from django.shortcuts import render

def protocolos_home(request):
    return render(request, 'protocolos/index.html')


