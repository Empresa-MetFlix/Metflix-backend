from rest_framework import viewsets
from core.models.reserva import Reserva
from core.serializers.reserva import ReservaSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
