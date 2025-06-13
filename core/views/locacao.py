from rest_framework import viewsets
from core.models.locacao import Locacao
from core.models.locacao_midia import LocacaoMidia
from core.serializers.locacao import LocacaoSerializer, LocacaoMidiaSerializer

class LocacaoViewSet(viewsets.ModelViewSet):
    queryset = Locacao.objects.all()
    serializer_class = LocacaoSerializer


class LocacaoMidiaViewSet(viewsets.ModelViewSet):
    queryset = LocacaoMidia.objects.all()
    serializer_class = LocacaoMidiaSerializer