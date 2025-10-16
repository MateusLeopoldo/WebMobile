from django.urls import path
from album.views import * 
urlpatterns = [
    path('', ListarAlbums.as_view(), name='listar-albums'),
    path('novo/', CriarAlbums.as_view(), name='criar-albums'),
    path('fotos/<str:arquivo>/', FotoAlbum.as_view(), name='foto-album'),
    path('editar/<int:pk>/', EditarAlbums.as_view(), name='editar-albums'),
    path('deletar/<int:pk>/', DeletarAlbums.as_view(), name='deletar-albums'),
]