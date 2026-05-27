from django.shortcuts import render, redirect
from .models import Paciente, Consulta, Conduta
from datetime import date
from django.utils import timezone


def dashboard(request):
    pacientes = Paciente.objects.filter(
        ultimo_acesso__isnull=False
    ).order_by('-ultimo_acesso')[:3]

    return render(
        request,
        'dashboard/index.html',
        {'pacientes': pacientes}
    )


def lista_pacientes(request):
    pacientes = Paciente.objects.all()

    return render(
        request,
        'dashboard/pacientes.html',
        {'pacientes': pacientes}
    )


def historico_paciente(request, id):
    paciente = Paciente.objects.get(id=id)

    paciente.ultimo_acesso = timezone.now()
    paciente.save()

    consulta_paciente = Consulta.objects.filter(
        paciente=paciente
    )

    return render(
        request,
        'dashboard/historico.html',
        {
            'paciente': paciente,
            'consultas': consulta_paciente
        }
    )


def prontuario_paciente(request, id):
    paciente = Paciente.objects.get(id=id)

    consulta = Consulta.objects.filter(
        paciente=paciente
    ).first()

    return render(
        request,
        'dashboard/prontuario.html',
        {
            'paciente': paciente,
            'consulta': consulta
        }
    )


def editar_paciente(request, id):
    paciente = Paciente.objects.get(id=id)

    consulta = Consulta.objects.filter(
        paciente=paciente
    ).first()

    if request.method == 'POST':

        nome = request.POST.get('nome_completo')
        data_nascimento = request.POST.get('data_nascimento')
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')

        erros = {}

        if not nome:
            erros['nome_completo'] = 'Nome completo é obrigatório.'
        if not data_nascimento:
            erros['data_nascimento'] = 'Data de nascimento é obrigatória.'
        if not peso:
            erros['peso'] = 'Peso é obrigatório.'
        if not altura:
            erros['altura'] = 'Altura é obrigatória.'

        if erros:
            return render(
                request,
                'dashboard/editar.html',
                {
                    'paciente': paciente,
                    'consulta': consulta,
                    'erros': erros,
                }
            )

        paciente.nome_completo = nome
        paciente.data_nascimento = data_nascimento
        paciente.peso = peso
        paciente.genero = request.POST.get('genero')
        paciente.altura = altura
        paciente.nome_mae = request.POST.get('nome_mae')
        paciente.nome_pai = request.POST.get('nome_pai')
        paciente.save()

        consulta.alergias = request.POST.get('alergias')
        consulta.doencas_cronicas = request.POST.get('doencas_cronicas')
        consulta.cirurgias_anteriores = request.POST.get('cirurgias_anteriores')
        consulta.medicamentos_uso_continuo = request.POST.get('medicamentos_uso_continuo')
        consulta.queixa_principal = request.POST.get('queixa_principal')
        consulta.historico_de_doenca_atual = request.POST.get('historico_doenca_atual')
        consulta.frequencia_respiratoria = request.POST.get('frequencia_respiratoria')
        consulta.pressao_arterial = request.POST.get('pressao_arterial')
        consulta.frequencia_cardiaca = request.POST.get('frequencia_cardiaca')
        consulta.temperatura = request.POST.get('temperatura')
        consulta.saturacao = request.POST.get('saturacao')
        consulta.ausculta_pulmonar = request.POST.get('ausculta_pulmonar')
        consulta.estado_geral = request.POST.get('estado_geral')
        consulta.exames_solicitados = request.POST.get('exames_solicitados')
        consulta.diagnostico_provisorio = request.POST.get('diagnostico_provisorio')
        consulta.save()

        # salva apenas as novas condutas adicionadas no front
        novas_condutas = request.POST.getlist('condutas[]')
        novas_criticas = request.POST.getlist('condutas_criticas[]')

        for i in range(len(novas_condutas)):
            descricao = novas_condutas[i].strip()

            if not descricao:
                continue

            critica = (novas_criticas[i] == 'true')

            Conduta.objects.create(
                consulta=consulta,
                descricao=descricao,
                critica=critica
            )

        return redirect('prontuario_paciente', id=paciente.id)

    return render(
        request,
        'dashboard/editar.html',
        {
            'paciente': paciente,
            'consulta': consulta
        }
    )


def cadastrar_paciente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome_completo')
        data_nascimento = request.POST.get('data_nascimento')
        peso = request.POST.get('peso')
        genero = request.POST.get('genero')
        altura = request.POST.get('altura')
        nome_mae = request.POST.get('nome_mae')
        nome_pai = request.POST.get('nome_pai')

        erros = {}

        if not nome:
            erros['nome_completo'] = 'Nome completo é obrigatório.'
        if not data_nascimento:
            erros['data_nascimento'] = 'Data de nascimento é obrigatória.'
        if not peso:
            erros['peso'] = 'Peso é obrigatório.'
        if not altura:
            erros['altura'] = 'Altura é obrigatória.'

        if erros:
            return render(
                request,
                'dashboard/cadastrar.html',
                {
                    'today': date.today(),
                    'erros': erros,
                    'dados': request.POST,
                }
            )

        paciente = Paciente.objects.create(
            nome_completo=nome,
            data_nascimento=data_nascimento,
            peso=peso,
            genero=genero,
            altura=altura,
            nome_mae=nome_mae,
            nome_pai=nome_pai
        )

        consulta = Consulta.objects.create(
            paciente=paciente,
            data_consulta=date.today(),
            alergias=request.POST.get('alergias'),
            doencas_cronicas=request.POST.get('doencas_cronicas'),
            cirurgias_anteriores=request.POST.get('cirurgias_anteriores'),
            medicamentos_uso_continuo=request.POST.get('medicamentos_uso_continuo'),
            queixa_principal=request.POST.get('queixa_principal'),
            historico_de_doenca_atual=request.POST.get('historico_doenca_atual'),
            frequencia_respiratoria=request.POST.get('frequencia_respiratoria'),
            pressao_arterial=request.POST.get('pressao_arterial'),
            frequencia_cardiaca=request.POST.get('frequencia_cardiaca'),
            temperatura=request.POST.get('temperatura'),
            saturacao=request.POST.get('saturacao'),
            ausculta_pulmonar=request.POST.get('ausculta_pulmonar'),
            estado_geral=request.POST.get('estado_geral'),
            exames_solicitados=request.POST.get('exames_solicitados'),
            diagnostico_provisorio=request.POST.get('diagnostico_provisorio'),
        )

        descricao_conduta = request.POST.get('descricao_conduta')
        critica = request.POST.get('critica') == 'on'

        if descricao_conduta:
            Conduta.objects.create(
                consulta=consulta,
                descricao=descricao_conduta,
                critica=critica
            )

        return redirect('dashboard')

    return render(
        request,
        'dashboard/cadastrar.html',
        {'today': date.today()}
    )