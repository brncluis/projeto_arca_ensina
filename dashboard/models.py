from django.db import models


class Paciente (models.Model):
    nome_completo = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    
    OPCOES =[
        ('M', 'Masculino'),
        ('F', 'Feminino')
    ]
    genero = models.CharField(max_length=1, choices=OPCOES)
    altura = models.DecimalField(max_digits=4, decimal_places=2)
    nome_mae = models.CharField(max_length=100)
    nome_pai = models.CharField(max_length=100)
    
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
    conduta_tratamento = models.TextField()
    medicamentos = models.ManyToManyField('protocolos.Medicamento', blank=True)

    def __str__(self):
        return f'{self.paciente.nome_completo} - {self.data_consulta}'