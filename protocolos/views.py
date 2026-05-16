from django.shortcuts import render
from .models import Protocolo, Categoria, Sintoma
from django.http import JsonResponse

def criar_dados_iniciais():
    if Categoria.objects.exists():
        return

    respiratorio = Categoria.objects.create(nome="Respiratório")
    cardiovascular = Categoria.objects.create(nome="Cardiovascular")
    geral = Categoria.objects.create(nome="Geral")
    gastrointestinal = Categoria.objects.create(nome="Gastrointestinal")

    # RESPIRATÓRIO
    Sintoma.objects.create(nome="Dispneia", categoria=respiratorio)
    Sintoma.objects.create(nome="Tosse", categoria=respiratorio)
    Sintoma.objects.create(nome="Chiado", categoria=respiratorio)
    Sintoma.objects.create(nome="Cianose", categoria=respiratorio)
    Sintoma.objects.create(nome="Apneia", categoria=respiratorio)

    # CARDIO
    Sintoma.objects.create(nome="Taquicardia", categoria=cardiovascular)
    Sintoma.objects.create(nome="Bradicardia", categoria=cardiovascular)
    Sintoma.objects.create(nome="Hipotensão", categoria=cardiovascular)

    # GERAL
    Sintoma.objects.create(nome="Febre", categoria=geral)
    Sintoma.objects.create(nome="Dor", categoria=geral)

    # GASTROINTESTINAL
    Sintoma.objects.create(nome="Diarreia", categoria=gastrointestinal)
    Sintoma.objects.create(nome="Distenção Abdominal", categoria=gastrointestinal)
    Sintoma.objects.create(nome="Vômito", categoria=gastrointestinal)


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
        "mensagem": mensagem
    })


def detalhes_protocolo(request):
    return render(request, 'protocolos/detalhes.html')


def fluxograma(request):
    return render(request, 'protocolos/fluxograma.html')

