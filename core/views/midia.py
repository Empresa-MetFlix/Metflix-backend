from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Midia
from core.serializers.midia import MidiaSerializer, MidiaDetailSerializer


class MidiaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar e visualizar mídias (filmes/séries).
    Apenas leitura para usuários.
    """
    queryset = Midia.objects.all()
    
    def get_serializer_class(self):
        """
        Usa serializer detalhado para retrieve/detail,
        serializer simples para list
        """
        if self.action == 'retrieve':
            return MidiaDetailSerializer
        return MidiaSerializer
    
    @action(detail=False, methods=['get'])
    def bombando(self, request):
        """
        Retorna mídias mais populares (bombando).
        Rota: /api/midias/bombando/
        """
        # TODO: Implementar lógica de popularidade (views, likes, etc)
        midias = self.get_queryset()[:10]  # Top 10
        serializer = self.get_serializer(midias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Busca mídias por título.
        Rota: /api/midias/search/?q=titulo
        """
        query = request.query_params.get('q', '')
        if query:
            midias = self.get_queryset().filter(titulo__icontains=query)
            serializer = self.get_serializer(midias, many=True)
            return Response(serializer.data)
        return Response([])
