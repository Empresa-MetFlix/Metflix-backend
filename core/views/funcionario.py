from rest_framework import viewsets
from core.models.funcionario import Funcionario
from core.serializers.funcionario import FuncionarioSerializer

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
