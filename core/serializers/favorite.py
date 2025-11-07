from rest_framework.serializers import ModelSerializer
from core.models import Favorite

class FavoriteSerializer(ModelSerializer):
    """
    Serializer para o modelo Favorite.
    Permite a representação e manipulação de objetos 'Favoritos'.
    """
    class Meta:
        model = Favorite
        # Campos que podem ser lidos e escritos via API
        fields = ('id', 'user', 'midia') 
        # Campos que são apenas leitura (se for o caso, 'id' geralmente é só leitura)
        read_only_fields = ('id',)