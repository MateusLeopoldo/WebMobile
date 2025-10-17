from django import forms
from django.forms import inlineformset_factory
from .models import Album, Musica


class FormularioAlbum(forms.ModelForm):
    class Meta:
        model = Album
        exclude = []
class FormularioMusica(forms.ModelForm):
    class Meta:
        model = Musica
        fields = ['titulo', 'duracao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da música'}),
            'duracao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM:SS'}),
        }

MusicaFormSet = inlineformset_factory(
    Album, Musica, form=FormularioMusica, extra=1, can_delete=True
)