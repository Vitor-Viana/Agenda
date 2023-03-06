from django.db import models
from django.contrib.auth.models import User

class Anotacao (models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_hora = models.DateTimeField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_data_hora(self):
        return self.data_hora.strftime('%d/%m/%Y %H:%M Hrs')

    def get_data_hora_input(self):
        return self.data_hora.strftime('%Y-%m-%dT%H:%M')

class CodigoRecuperacao(models.Model):
    codigo = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
