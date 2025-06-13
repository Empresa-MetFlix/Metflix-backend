from rest_framework import viewsets
from core.models.cliente import Cliente
from core.serializers.cliente import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
