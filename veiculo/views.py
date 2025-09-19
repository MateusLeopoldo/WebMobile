# -*- coding: utf-8 -*-
from django.views.generic import ListView
from veiculo.models import Veiculo
from datetime import datetime

class ListarVeiculos(ListView):
    """
    View para listar veiculos cadastrados.
    """
    model = Veiculo
    context_object_name = 'lista_veiculos'
    template_name = 'veiculo/listar.html'

    def get_queryset(self):
        data_atual = datetime.now()
        return Veiculo.objects.filter()