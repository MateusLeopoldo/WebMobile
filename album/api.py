from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from album.models import Album
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin   
from album.forms import FormularioAlbum, MusicaFormSet
from django.http import FileResponse, Http404, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import AlbumSerializer, AlbumListSerializer
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Album
from .serializers import AlbumListSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_albums_api(request):
    """
    API endpoint para listar álbuns com filtros opcionais.
    
    Parâmetros de query:
    - q: busca por título ou artista
    - genero: filtro por gênero
    - ano: filtro por ano de lançamento
    - formato: filtro por formato
    """
    queryset = Album.objects.all()
    
    # Aplicar filtros
    q = request.GET.get('q')
    genero = request.GET.get('genero')
    ano = request.GET.get('ano')
    formato = request.GET.get('formato')
    
    if q:
        queryset = queryset.filter(titulo__icontains=q) | queryset.filter(artista__icontains=q)
    if genero:
        queryset = queryset.filter(genero=genero)
    if ano:
        queryset = queryset.filter(ano_lancamento=ano)
    if formato:
        queryset = queryset.filter(formato=formato)
    
    queryset = queryset.order_by('-id')
    
    # Usar serializer simplificado para listagem ou completo para detalhes
    detalhado = request.GET.get('detalhado', 'false').lower() == 'true'
    
    if detalhado:
        serializer = AlbumSerializer(queryset, many=True, context={'request': request})
    else:
        serializer = AlbumListSerializer(queryset, many=True, context={'request': request})
    
    return Response({
        'count': queryset.count(),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalhe_album_api(request, pk):
    """
    API endpoint para obter detalhes completos de um álbum específico.
    """
    try:
        album = Album.objects.get(pk=pk)
        serializer = AlbumSerializer(album, context={'request': request})
        return Response(serializer.data)
    except Album.DoesNotExist:
        return Response(
            {'error': 'Álbum não encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )


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

class LoginJWT(TokenObtainPairView):
    permission_classes = [AllowAny]

class RefreshJWT(TokenRefreshView):
    permission_classes = [AllowAny]

class APIListarAlbums(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Album.objects.all().order_by('-id')
        q = request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(titulo__icontains=q) | Q(artista__icontains=q))
        serializer = AlbumListSerializer(queryset, many=True, context={'request': request})
        return Response({'count': queryset.count(), 'results': serializer.data})