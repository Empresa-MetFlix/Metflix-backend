from rest_framework import viewsets
from core.models.pagamento import Pagamento
from core.serializers.pagamento import PagamentoSerializer

class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
