from django.db import models
from django.contrib.auth.models import AbstractUser

import random


class Usuario(AbstractUser):

    # ID único usado para login
    id_acesso = models.CharField(
        max_length=6,
        unique=True,
        blank=True
    )

    USERNAME_FIELD = 'id_acesso'

    REQUIRED_FIELDS = ['username', 'email']

    def gerar_id(self):

        while True:

            novo_id = str(
                random.randint(100000, 999999)
            )

            # verifica se já existe
            if not Usuario.objects.filter(
                id_acesso=novo_id
            ).exists():

                return novo_id

    def save(self, *args, **kwargs):

        # gera ID automaticamente
        if not self.id_acesso:

            self.id_acesso = self.gerar_id()

        super().save(*args, **kwargs)

    def __str__(self):

        return f'{self.username} ({self.id_acesso})'