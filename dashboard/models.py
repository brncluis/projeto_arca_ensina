from django.db import models
from django.conf import settings #Leticia: Biblioteca para relacionar o usuario ao paciente exportado


class Paciente (models.Model):
    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    
    OPCOES =[
        ('M', 'Masculino'),
        ('F', 'Feminino')
    ]
    genero = models.CharField(max_length=1, choices=OPCOES)
    altura = models.DecimalField(max_digits=3, decimal_places=0)
    nome_mae = models.CharField(max_length=100)
    nome_pai = models.CharField(max_length=100)
    ultimo_acesso = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.nome_completo
    
class Consulta (models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_consulta = models.DateField()
    alergias = models.TextField()
    doencas_cronicas = models.TextField()
    cirurgias_anteriores = models.TextField()
    medicamentos_uso_continuo = models.TextField()
    queixa_principal = models.CharField(max_length=200)
    historico_de_doenca_atual = models.TextField()
    frequencia_respiratoria = models.CharField(max_length=50)
    pressao_arterial = models.CharField(max_length=50)
    frequencia_cardiaca = models.CharField(max_length=50)
    temperatura = models.CharField(max_length=50)
    saturacao = models.CharField(max_length=50)
    ausculta_pulmonar = models.CharField(max_length=50)
    estado_geral = models.CharField(max_length=50)
    exames_solicitados = models.CharField(max_length=100)
    diagnostico_provisorio = models.CharField(max_length=100)
    #conduta_tratamento = models.TextField()
    medicamentos = models.ManyToManyField('protocolos.Medicamento', blank=True)

    protocolos_utilizados = models.ManyToManyField(
    'protocolos.Protocolo',
    blank=True
    )

    def __str__(self):
        return f'{self.paciente.nome_completo} - {self.data_consulta}'


#Davi: Criei essa classe para salvar as Condutas Críticas dos pacientes
class Conduta(models.Model):

    consulta = models.ForeignKey(
        Consulta,
        on_delete=models.CASCADE,
        related_name='condutas'
    )

    descricao = models.TextField()

    critica = models.BooleanField(default=False)

    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao

class Medico(models.Model):
    
    nome = models.CharField(max_length=200)
    crm  = models.CharField(max_length=20, blank=True)
    especialidade = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'

    def __str__(self):
        return self.nome


class PacienteExportado(models.Model):
    
    paciente       = models.ForeignKey(
        'Paciente',                          # seu modelo de Paciente
        on_delete=models.CASCADE,
        related_name='exportacoes',
        verbose_name='Paciente',
    )
    medico_destino = models.ForeignKey(
        Medico,
        on_delete=models.SET_NULL,
        null=True,
        related_name='pacientes_recebidos',
        verbose_name='Médico destino',
    )
    exportado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='exportacoes_realizadas',
        verbose_name='Exportado por',
    )
    data_exportacao = models.DateTimeField(auto_now_add=True, verbose_name='Data da exportação')

    class Meta:
        ordering = ['-data_exportacao']
        verbose_name = 'Paciente Exportado'
        verbose_name_plural = 'Pacientes Exportados'

    def __str__(self):
        medico = self.medico_destino.nome if self.medico_destino else 'Médico removido'
        return f'{self.paciente} → {medico} ({self.data_exportacao:%d/%m/%Y %H:%M})'