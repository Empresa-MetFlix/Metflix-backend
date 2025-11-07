from rest_framework import serializers
from core.models import LocacaoMidia

class LocacaoMidiaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo LocacaoMidia.
    Este modelo geralmente representa os itens (mídias) dentro de uma locação.
    """
    class Meta:
        model = LocacaoMidia
        fields = ('id', 'locacao', 'midia', 'quantidade', 'preco_unitario')
        read_only_fields = ('id',)