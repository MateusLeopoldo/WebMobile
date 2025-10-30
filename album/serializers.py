from rest_framework import serializers
from album.models import Album

class SerializadorAlbum(serializers.ModelSerializer):
    """
    Serializador para o modelo Album
    """
    class Meta:
        model = Album
        exclude = []  