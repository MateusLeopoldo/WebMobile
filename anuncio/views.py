from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Anuncio
from .forms import AnuncioForm

class SuperuserRequiredMixin(UserPassesTestMixin):
    """Garante que o usuário seja um superusuário."""
    def test_func(self):
        return self.request.user.is_superuser

class ListarAnuncios(ListView):
    model = Anuncio
    template_name = 'anuncio/listar_anuncios.html'
    context_object_name = 'anuncios'

class CriarAnuncio(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    model = Anuncio
    form_class = AnuncioForm
    template_name = 'anuncio/form_anuncio.html'
    success_url = reverse_lazy('listar-anuncios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Criar Novo Anúncio'
        return context

class EditarAnuncio(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    model = Anuncio
    form_class = AnuncioForm
    template_name = 'anuncio/form_anuncio.html'
    success_url = reverse_lazy('listar-anuncios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Editar Anúncio'
        return context

class DeletarAnuncio(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = Anuncio
    template_name = 'anuncio/deletar_anuncio.html'
    success_url = reverse_lazy('listar-anuncios')
from django.shortcuts import render

# Create your views here.
