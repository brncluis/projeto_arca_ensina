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