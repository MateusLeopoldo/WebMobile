from rest_framework import serializers
from .models import Album, Musica
from album.consts import OPCOES_GENERO, OPCOES_ALBUM, OPCOES_FORMATO, OPCOES_IDIOMA


class MusicaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Musica"""
    duracao_formatada = serializers.SerializerMethodField()
    
    class Meta:
        model = Musica
        fields = ['id', 'titulo', 'duracao', 'duracao_formatada']
    
    def get_duracao_formatada(self, obj):
        """Retorna a duração formatada em MM:SS"""
        if obj.duracao:
            total_seconds = int(obj.duracao.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes:02d}:{seconds:02d}"
        return "00:00"


class SerializadorAlbum(serializers.ModelSerializer):
    """
    Serializador para o modelo Album
    """
    class Meta:
        model = Album
        exclude = []


class AlbumSerializer(serializers.ModelSerializer):
    """Serializer completo para o modelo Album"""
    musicas = MusicaSerializer(many=True, read_only=True)
    genero_display = serializers.SerializerMethodField()
    tipo_album_display = serializers.SerializerMethodField()
    formato_display = serializers.SerializerMethodField()
    idioma_display = serializers.SerializerMethodField()
    duracao_total = serializers.SerializerMethodField()
    duracao_total_formatada = serializers.SerializerMethodField()
    e_novo = serializers.SerializerMethodField()
    anos_desde_lancamento = serializers.SerializerMethodField()
    foto_url = serializers.SerializerMethodField()
    preco_formatado = serializers.SerializerMethodField()
    quantidade_musicas = serializers.SerializerMethodField()
    
    class Meta:
        model = Album
        fields = [
            'id',
            'titulo',
            'descricao',
            'artista',
            'genero',
            'genero_display',
            'ano_lancamento',
            'tipo_album',
            'tipo_album_display',
            'formato',
            'formato_display',
            'idioma',
            'idioma_display',
            'preco',
            'preco_formatado',
            'foto',
            'foto_url',
            'musicas',
            'duracao_total',
            'duracao_total_formatada',
            'quantidade_musicas',
            'e_novo',
            'anos_desde_lancamento',
        ]
    
    def get_genero_display(self, obj):
        """Retorna o nome legível do gênero"""
        return dict(OPCOES_GENERO).get(obj.genero, 'Desconhecido')
    
    def get_tipo_album_display(self, obj):
        """Retorna o nome legível do tipo de álbum"""
        return dict(OPCOES_ALBUM).get(obj.tipo_album, 'Desconhecido')
    
    def get_formato_display(self, obj):
        """Retorna o nome legível do formato"""
        return dict(OPCOES_FORMATO).get(obj.formato, 'Desconhecido')
    
    def get_idioma_display(self, obj):
        """Retorna o nome legível do idioma"""
        return dict(OPCOES_IDIOMA).get(obj.idioma, 'Desconhecido')
    
    def get_duracao_total(self, obj):
        """Retorna a duração total em segundos"""
        duracao = obj.duracao_total
        return int(duracao.total_seconds()) if duracao else 0
    
    def get_duracao_total_formatada(self, obj):
        """Retorna a duração total formatada"""
        duracao = obj.duracao_total
        if duracao:
            total_seconds = int(duracao.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            return f"{minutes:02d}:{seconds:02d}"
        return "00:00"
    
    def get_e_novo(self, obj):
        """Retorna se o álbum é novo"""
        return obj.e_novo()
    
    def get_anos_desde_lancamento(self, obj):
        """Retorna quantos anos desde o lançamento"""
        return obj.anos_desde_lancamento()
    
    def get_foto_url(self, obj):
        """Retorna a URL completa da foto"""
        if obj.foto:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto.url)
            return obj.foto.url
        return None
    
    def get_preco_formatado(self, obj):
        """Retorna o preço formatado"""
        return f"R$ {obj.preco:.2f}"
    
    def get_quantidade_musicas(self, obj):
        """Retorna a quantidade de músicas"""
        return obj.musicas.count()


class AlbumListSerializer(serializers.ModelSerializer):
    foto_url = serializers.SerializerMethodField()
    preco_formatado = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ['id', 'titulo', 'artista', 'ano_lancamento', 'preco', 'preco_formatado', 'foto_url']

    def get_foto_url(self, obj):
        request = self.context.get('request')
        if getattr(obj, 'foto', None):
            return request.build_absolute_uri(obj.foto.url) if request else obj.foto.url
        return None

    def get_preco_formatado(self, obj):
        return f"R$ {obj.preco:.2f}" if obj.preco is not None else None