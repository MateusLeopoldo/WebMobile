# -*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from veiculo.models import Veiculo
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin   
from veiculo.forms import FormularioVeiculo 
from django.views import View
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist


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

class FotoVeiculo(View):

    def get(self, request, arquivo):
        try: 
            veiculo = Veiculo.objects.get(foto='veiculo/fotos/{}'.format(arquivo))
            return FileResponse(veiculo.foto)
        except ObjectDoesNotExist:
            raise Http404("Foto não encontrada ou acesso negado.")
        except Exception as exception:
            raise exception
        
class EditarVeiculos(LoginRequiredMixin , UpdateView):
    model = Veiculo
    form_class = FormularioVeiculo
    template_name = 'veiculo/editar.html'
    success_url = reverse_lazy('listar-veiculos')

class DeletarVeiculos(LoginRequiredMixin , DeleteView):
    model = Veiculo
    template_name = 'veiculo/deletar.html'
    success_url = reverse_lazy('listar-veiculos')
