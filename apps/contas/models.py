from django.db import models
from django.contrib.auth.models import User

class PasswordReset(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário', related_name='resets')
    key = models.CharField(max_length=100, unique=True, verbose_name='Chave')
    data_criacao = models.DateTimeField('Criado em', auto_now_add=True)
    confirmacao = models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} em {1}'.format(self.user, self.data_criacao)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas senhas'
        ordering = ['-data_criacao']