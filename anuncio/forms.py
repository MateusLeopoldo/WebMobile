from django import forms
from .models import Anuncio

class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['titulo', 'descricao', 'albums']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'albums': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '10'}),
        }
        help_texts = {
            'albums': 'Segure "Ctrl" (ou "Cmd" no Mac) para selecionar mais de um álbum.',
        }
