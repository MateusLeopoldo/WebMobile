from django.db import models
from album.consts import OPCOES_GENERO, OPCOES_ALBUM, OPCOES_FORMATO, OPCOES_IDIOMA
from datetime import timedelta
from django.utils import timezone

class Album(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    genero = models.IntegerField(choices=OPCOES_GENERO)
    ano_lancamento = models.IntegerField()
    artista = models.CharField(max_length=100)
    tipo_album = models.IntegerField(choices=OPCOES_ALBUM)
    formato = models.IntegerField(choices=OPCOES_FORMATO)
    idioma = models.IntegerField(choices=OPCOES_IDIOMA)
    foto = models.ImageField(upload_to='album/fotos', null=True, blank=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    @property
    def duracao_total(self):
        """Calcula a duração total do álbum somando a duração de todas as suas músicas."""
        total_seconds = sum(m.duracao.total_seconds() for m in self.musicas.all() if m.duracao)
        return timedelta(seconds=total_seconds)
    
    def e_novo(self):
        return self.ano_lancamento >= timezone.now().year

    def anos_desde_lancamento(self):
        return timezone.now().year - self.ano_lancamento

    def __str__(self):
        return self.titulo

class Musica(models.Model):
    album = models.ForeignKey(Album, related_name='musicas', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    duracao = models.DurationField()
    
    class Meta:
        verbose_name_plural = "Musicas"
    
    def __str__(self):
        return self.titulo
    
    