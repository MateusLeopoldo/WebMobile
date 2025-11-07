from django.urls import path
from album.views import * 
from album.api import APIListarAlbums, LoginJWT, RefreshJWT

urlpatterns = [
    path('', ListarAlbums.as_view(), name='listar-albums'),
    path('novo/', CriarAlbums.as_view(), name='criar-albums'),
    path('fotos/<str:arquivo>/', FotoAlbum.as_view(), name='foto-album'),
    path('editar/<int:pk>/', EditarAlbums.as_view(), name='editar-albums'),
    path('deletar/<int:pk>/', DeletarAlbums.as_view(), name='deletar-albums'),

    # APIs mobile
    path('api/albums/', APIListarAlbums.as_view(), name='api-listar-albums'),
    path('api/', APIListarAlbums.as_view(), name='api-listar-albums-compat'),  # compat

    # Auth JWT (login/refresh)
    path('api/auth/login/', LoginJWT.as_view(), name='api-auth-login'),
    path('api/auth/refresh/', RefreshJWT.as_view(), name='api-auth-refresh'),
]
