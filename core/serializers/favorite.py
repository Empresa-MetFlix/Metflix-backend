from rest_framework import serializers
from core.models import Favorite
from core.serializers.midia import MidiaSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer para favoritos com dados da mídia aninhados"""
    midia = MidiaSerializer(read_only=True)
    midia_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'midia', 'midia_id', 'adicionado_em']
        read_only_fields = ['user', 'adicionado_em']
    
    def validate_midia_id(self, value):
        """Valida se a mídia existe"""
        from core.models import Midia
        if not Midia.objects.filter(id=value).exists():
            raise serializers.ValidationError("Mídia não encontrada.")
        return value
