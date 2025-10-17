from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from album.models import Album
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin   
from album.forms import FormularioAlbum, MusicaFormSet
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

class ListarAlbums(LoginRequiredMixin , ListView):
    model = Album
    context_object_name = 'lista_albums'
    template_name = 'album/listar.html'

    def get_queryset(self):
        queryset = Album.objects.all()
        q = self.request.GET.get('q')
        genero = self.request.GET.get('genero')
        ano = self.request.GET.get('ano')

        if q:
            queryset = queryset.filter(titulo__icontains=q) | queryset.filter(artista__icontains=q)
        if genero:
            queryset = queryset.filter(genero=genero)
        if ano:
            queryset = queryset.filter(ano_lancamento=ano)
        
        return queryset.order_by('-id')
    
class CriarAlbums(LoginRequiredMixin , CreateView):
    model = Album
    form_class = FormularioAlbum
    template_name = 'album/novo.html'
    success_url = reverse_lazy('listar-albums')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['musicas'] = MusicaFormSet(self.request.POST, self.request.FILES)
        else:
            data['musicas'] = MusicaFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        musicas = context['musicas']
        if musicas.is_valid():
            with transaction.atomic():
                self.object = form.save()
                musicas.instance = self.object # Associa o formset ao álbum recém-criado
                musicas.save() # Salva as músicas
                return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form, musicas=musicas))


class FotoAlbum(View):

    def get(self, request, arquivo):
        try: 
            album = Album.objects.get(foto='album/fotos/{}'.format(arquivo))
            return FileResponse(album.foto)
        except ObjectDoesNotExist:
            raise Http404("Foto não encontrada ou acesso negado.")
        except Exception as exception:
            raise exception
        
class EditarAlbums(LoginRequiredMixin , UpdateView):
    model = Album
    form_class = FormularioAlbum
    template_name = 'album/editar.html'
    success_url = reverse_lazy('listar-albums')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['musicas'] = MusicaFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['musicas'] = MusicaFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        musicas = context['musicas']
        with transaction.atomic():
            self.object = form.save()
            if musicas.is_valid():
                musicas.instance = self.object
                musicas.save()
        return redirect(self.get_success_url())

class DeletarAlbums(LoginRequiredMixin , DeleteView):
    model = Album
    template_name = 'album/deletar.html'
    success_url = reverse_lazy('listar-albums')
