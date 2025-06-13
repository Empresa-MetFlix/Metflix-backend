from rest_framework import serializers
from core.models.locacao import Locacao
from core.models.locacao_midia import LocacaoMidia

class LocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locacao
        fields = '__all__'


class LocacaoMidiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocacaoMidia
        fields = '__all__'