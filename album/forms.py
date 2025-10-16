from django.forms import ModelForm
from .models import Album, Musica
from django import forms
from django.forms import inlineformset_factory, TimeInput

class FormularioAlbum(ModelForm):
    class Meta:
        model = Album
        fields = ['titulo', 'descricao', 'genero', 'ano_lancamento', 'artista', 'tipo_album', 'formato', 'idioma', 'foto', 'preco']

class MusicaForm(ModelForm):
    class Meta:
        model = Musica
        fields = ['titulo', 'duracao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da música'}),
            'duracao': TimeInput(attrs={'class': 'form-control', 'placeholder': '00:03:45', 'type': 'time'}),
        }

MusicaFormSet = inlineformset_factory(
    Album,
    Musica,
    form=MusicaForm,
    extra=1,
    can_delete=True
)