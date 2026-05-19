from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Sintoma(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Protocolo(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)

    sintomas = models.ManyToManyField(Sintoma, blank=True)

    def __str__(self):
        return self.titulo
    
class Medicamento(models.Model):
    nomes = models.CharField(max_length=50)
    dosagens_minima = models.DecimalField(max_digits=5, decimal_places=3)
    dosagens_maxima = models.DecimalField(max_digits=6, decimal_places=3)
    unidades_dosagem = models.CharField(max_length=50)

    def __str__(self):
        return self.nome