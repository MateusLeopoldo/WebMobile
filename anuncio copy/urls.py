from django.urls import path
from .views import ListarAnuncios, CriarAnuncio, EditarAnuncio, DeletarAnuncio

urlpatterns = [
    path('', ListarAnuncios.as_view(), name='listar-anuncios'),
    path('novo/', CriarAnuncio.as_view(), name='criar-anuncio'),
    path('editar/<int:pk>/', EditarAnuncio.as_view(), name='editar-anuncio'),
    path('deletar/<int:pk>/', DeletarAnuncio.as_view(), name='deletar-anuncio'),
]
