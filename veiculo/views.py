# -*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from veiculo.models import Veiculo
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin   
from veiculo.forms import FormularioVeiculo

class ListarVeiculos(LoginRequiredMixin , ListView):
    """
    View para listar veiculos cadastrados.
    """
    model = Veiculo
    context_object_name = 'lista_veiculos'
    template_name = 'veiculo/listar.html'

    def get_queryset(self):
        data_atual = datetime.now()
        return Veiculo.objects.filter()


class CriarVeiculos(LoginRequiredMixin , CreateView):
    model = Veiculo
    form_class = FormularioVeiculo
    template_name = 'veiculo/novo.html'
    success_url = reverse_lazy('listar-veiculos')