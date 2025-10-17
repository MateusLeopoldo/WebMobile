from django.db import models

# Create your models here.
from django.db import models
from album.models import Album

class Anuncio(models.Model):
    titulo = models.CharField(max_length=100, help_text="Ex: 'Novidades do Rock Progressivo'")
    descricao = models.TextField(blank=True, null=True, help_text="Uma breve descrição sobre esta coleção de álbuns.")
    albums = models.ManyToManyField(Album, related_name="anuncios")
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = "Anúncio"
        verbose_name_plural = "Anúncios"

    def __str__(self):
        return self.titulo
