from rest_framework import viewsets
from core.models.genero import Genero
from core.serializers.genero import GeneroSerializer

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
