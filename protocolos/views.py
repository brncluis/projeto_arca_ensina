from django.shortcuts import render
from .models import Protocolo, Categoria, Sintoma


def criar_dados_iniciais():
    respiratorio, _ = Categoria.objects.get_or_create(nome="Respiratório")
    cardiovascular, _ = Categoria.objects.get_or_create(nome="Cardiovascular")
    geral, _ = Categoria.objects.get_or_create(nome="Geral")
    gastrointestinal, _ = Categoria.objects.get_or_create(nome="Gastrointestinal")

    sintomas = [
        ("Dispneia", respiratorio),
        ("Tosse", respiratorio),
        ("Chiado", respiratorio),
        ("Cianose", respiratorio),
        ("Apneia", respiratorio),
        ("Taquicardia", cardiovascular),
        ("Bradicardia", cardiovascular),
        ("Hipotensão", cardiovascular),
        ("Febre", geral),
        ("Dor", geral),
        ("Diarreia", gastrointestinal),
        ("Distenção Abdominal", gastrointestinal),
        ("Vômito", gastrointestinal),
    ]

    for nome, categoria in sintomas:
        Sintoma.objects.get_or_create(nome=nome, categoria=categoria)


def protocolos_home(request):
    criar_dados_iniciais()

    sintomas_ids = request.GET.getlist("sintomas")

    if sintomas_ids:
        protocolos = Protocolo.objects.filter(
            sintomas__id__in=sintomas_ids
        ).distinct()
    else:
        protocolos = Protocolo.objects.all()

    categorias = Categoria.objects.all()

    mensagem = None
    if sintomas_ids and not protocolos.exists():
        mensagem = "Nenhum protocolo encontrado com esses sintomas"

    return render(request, 'protocolos/index.html', {
        'protocolos': protocolos,
        'categorias': categorias,
        'mensagem': mensagem,
    })


def detalhes_protocolo(request):
    categorias = Categoria.objects.all()
    return render(request, 'protocolos/detalhes.html', {
        'categorias': categorias,
    })

def detalhes_protocolo_sedacao(request):
    return render(request, 'protocolos/detalhes_sedacao.html')

def fluxograma(request):
    categorias = Categoria.objects.all()
    return render(request, 'protocolos/fluxograma.html', {
        'categorias': categorias,
    })

def fluxograma_sedacao(request):
    return render(request, 'protocolos/fluxograma_sedacao.html')
