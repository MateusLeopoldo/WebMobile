from django.db import models
from veiculo.consts import OPCOES_MARCA, OPCOES_COR, OPCOES_COMBUSTIVEL

class Veiculo(models.Model):
    marca = models.SmallIntegerField(choices=OPCOES_MARCA)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    cor = models.SmallIntegerField(choices=OPCOES_COR)
    combustivel = models.SmallIntegerField(choices=OPCOES_COMBUSTIVEL)
    foto = models.ImageField(upload_to='veiculo/fotos', null=True, blank=True)