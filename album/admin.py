from django.contrib import admin
from .models import Album, Musica

class MusicaInline(admin.TabularInline):
    model = Musica
    extra = 1

class AlbumAdmin(admin.ModelAdmin):
    inlines = [MusicaInline]
    list_display = ('titulo', 'artista', 'genero', 'preco')
    search_fields = ('titulo', 'artista')

admin.site.register(Album, AlbumAdmin)
