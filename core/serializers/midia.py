from rest_framework import serializers
from core.models import Midia, Genero # Assumindo que Genero e Midia são modelos existentes

# Serializer base para o modelo Genero (necessário para a representação aninhada)
class GeneroSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Genero."""
    class Meta:
        model = Genero
        fields = ('id', 'nome')

# Serializer simples da Midia (para listagens rápidas)
class MidiaSerializer(serializers.ModelSerializer):
    """
    Serializer básico para o modelo Midia, usado em listagens.
    """
    class Meta:
        model = Midia
        fields = '__all__'

# Serializer detalhado da Midia (para fixar o erro de importação)
class MidiaDetailSerializer(serializers.ModelSerializer):
    """
    Serializer detalhado para o modelo Midia.
    Inclui a representação do campo 'genero' aninhada.
    """
    # Assume que o campo 'genero' em Midia é um relacionamento (ForeignKey ou ManyToMany)
    genero = GeneroSerializer(many=True, read_only=True) 
    
    class Meta:
        model = Midia
        # Inclua todos os campos necessários. Ajuste conforme seu modelo Midia.
        fields = ('id', 'titulo', 'lancamento', 'sinopse', 'duracao', 'link', 'genero')