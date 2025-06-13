from rest_framework import viewsets
from core.models.midia import Midia
from core.serializers.midia import MidiaSerializer

class MidiaViewSet(viewsets.ModelViewSet):
    queryset = Midia.objects.all()
    serializer_class = MidiaSerializer