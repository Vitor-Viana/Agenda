from django.db import models

class Anotacao (models.Model):
    titulo = models.CharField (max_length=100)
    descricao = models.TextField (blank=True, null=True)
    data_hora = models.DateTimeField ()
