from django.shortcuts import render, redirect, get_object_or_404

from .models import Protocolo, Categoria, Sintoma
from dashboard.models import Paciente, Consulta


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

    dengue, _ = Protocolo.objects.get_or_create(
        titulo="Dengue",
        defaults={
            "descricao": "Uma doença infecciosa febril aguda, transmitida pela picada da fêmea do mosquito Aedes aegypti."
        }
    )

    sintomas_dengue = Sintoma.objects.filter(
        nome__in=["Febre", "Dor", "Vômito"]
    )

    dengue.sintomas.set(sintomas_dengue)

    sedacao, _ = Protocolo.objects.get_or_create(
        titulo="Sedação",
        defaults={
            "descricao": "Protocolo de sedação para procedimentos clínicos."
        }
    )

    sintomas_sedacao = Sintoma.objects.filter(
        nome__in=["Apneia", "Bradicardia", "Hipotensão"]
    )

    sedacao.sintomas.set(sintomas_sedacao)


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
        'sintomas_selecionados': sintomas_ids,
    })


def detalhes_protocolo(request):
    criar_dados_iniciais()

    protocolo = get_object_or_404(
        Protocolo,
        titulo="Dengue"
    )

    categorias = Categoria.objects.all()

    pacientes = Paciente.objects.filter(
        consulta__isnull=False
    ).distinct().order_by('-ultimo_acesso', 'nome_completo')

    return render(request, 'protocolos/detalhes.html', {
        'categorias': categorias,
        'protocolo': protocolo,
        'pacientes': pacientes,
    })


def detalhes_protocolo_sedacao(request):
    criar_dados_iniciais()

    protocolo = get_object_or_404(
        Protocolo,
        titulo="Sedação"
    )

    categorias = Categoria.objects.all()

    pacientes = Paciente.objects.filter(
        consulta__isnull=False
    ).distinct().order_by('-ultimo_acesso', 'nome_completo')

    return render(request, 'protocolos/detalhes_sedacao.html', {
        'categorias': categorias,
        'protocolo': protocolo,
        'pacientes': pacientes,
    })


def mesclar_paciente(request, protocolo_id, paciente_id):
    protocolo = get_object_or_404(
        Protocolo,
        id=protocolo_id
    )

    paciente = get_object_or_404(
        Paciente,
        id=paciente_id
    )

    consulta = Consulta.objects.filter(
        paciente=paciente
    ).first()

    if consulta:
        consulta.protocolos_utilizados.add(protocolo)

    return redirect(request.META.get('HTTP_REFERER', 'protocolos'))


def fluxograma(request):
    criar_dados_iniciais()

    protocolo = get_object_or_404(
        Protocolo,
        titulo="Dengue"
    )

    categorias = Categoria.objects.all()

    pacientes = Paciente.objects.filter(
        consulta__isnull=False
    ).distinct().order_by(
        '-ultimo_acesso',
        'nome_completo'
    )

    return render(request, 'protocolos/fluxograma.html', {
        'categorias': categorias,
        'protocolo': protocolo,
        'pacientes': pacientes,
    })


def fluxograma_sedacao(request):
    criar_dados_iniciais()

    protocolo = get_object_or_404(
        Protocolo,
        titulo="Sedação"
    )

    categorias = Categoria.objects.all()

    pacientes = Paciente.objects.filter(
        consulta__isnull=False
    ).distinct().order_by(
        '-ultimo_acesso',
        'nome_completo'
    )

    return render(request, 'protocolos/fluxograma_sedacao.html', {
        'categorias': categorias,
        'protocolo': protocolo,
        'pacientes': pacientes,
    })


def calculadora_dosagens(request):
    return render(request, 'protocolos/calculadora.html')