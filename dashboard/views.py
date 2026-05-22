from django.shortcuts import render, redirect
from .models import Paciente, Consulta
from datetime import date

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

def cadastrar_paciente(request):
    if request.method == 'POST': 
        nome = request.POST.get('nome_completo')
        data_nascimento = request.POST.get('data_nascimento')
        peso = request.POST.get('peso')
        genero = request.POST.get('genero')
        altura = request.POST.get('altura')
        nome_mae = request.POST.get('nome_mae')
        nome_pai = request.POST.get('nome_pai') 
        
        paciente = Paciente.objects.create(
            nome_completo=nome,
            data_nascimento=data_nascimento,
            peso=peso,
            genero=genero,
            altura=altura,
            nome_mae=nome_mae,
            nome_pai=nome_pai
        )
    
        alergias = request.POST.get('alergias')
        doencas_cronicas = request.POST.get('doencas_cronicas')
        cirurgias_anteriores = request.POST.get('cirurgias_anteriores')
        medicamentos_uso_continuo = request.POST.get('medicamentos_uso_continuo')
        queixa_principal = request.POST.get('queixa_principal')
        historico_doenca_atual = request.POST.get('historico_doenca_atual')
        frequencia_respiratoria = request.POST.get('frequencia_respiratoria')
        pressao_arterial = request.POST.get('pressao_arterial')
        frequencia_cardiaca = request.POST.get('frequencia_cardiaca')
        temperatura = request.POST.get('temperatura')
        saturacao = request.POST.get('saturacao')
        ausculta_pulmonar = request.POST.get('ausculta_pulmonar')
        estado_geral = request.POST.get('estado_geral')
        exames_solicitados = request.POST.get('exames_solicitados')
        diagnostico_provisorio = request.POST.get('diagnostico_provisorio')
        conduta_tratamento = request.POST.get('conduta_tratamento')

        Consulta.objects.create(
            paciente=paciente,
            data_consulta=date.today(),
            alergias=alergias,
            doencas_cronicas=doencas_cronicas,
            cirurgias_anteriores=cirurgias_anteriores,
            medicamentos_uso_continuo=medicamentos_uso_continuo,
            queixa_principal=queixa_principal,
            historico_de_doenca_atual=historico_doenca_atual,
            frequencia_respiratoria=frequencia_respiratoria,
            pressao_arterial=pressao_arterial,
            frequencia_cardiaca=frequencia_cardiaca,
            temperatura=temperatura,
            saturacao=saturacao,
            ausculta_pulmonar=ausculta_pulmonar,
            estado_geral=estado_geral,
            exames_solicitados=exames_solicitados,
            diagnostico_provisorio=diagnostico_provisorio,
            conduta_tratamento=conduta_tratamento,
        )

        return redirect('dashboard')
    
    return render(request, 'dashboard/cadastrar.html', {'today': date.today()})
        