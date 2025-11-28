from .user import UserSerializer
from .cliente import ClienteSerializer
from .funcionario import FuncionarioSerializer
from .genero import GeneroSerializer
from .midia import MidiaSerializer, MidiaDetailSerializer
from .locacao import LocacaoSerializer, LocacaoMidiaSerializer
from .pagamento import PagamentoSerializer
from .reserva import ReservaSerializer
from .favorite import FavoriteSerializer
from .token import CustomTokenObtainPairSerializer
from .profile import ProfileSerializer  # NOVO SERIALIZER PARA PROFILE
from .notification import NotificationSerializer  # NOVO SERIALIZER PARA NOTIFICATION

__all__ = [
    'UserSerializer',
    'ClienteSerializer',
    'FuncionarioSerializer',
    'GeneroSerializer',
    'MidiaSerializer',
    'MidiaDetailSerializer',
    'LocacaoSerializer',
    'LocacaoMidiaSerializer',
    'PagamentoSerializer',
    'ReservaSerializer',
    'FavoriteSerializer',
    'CustomTokenObtainPairSerializer',
    'ProfileSerializer',  # ADICIONAR AQUI TAMBÉM
    'NotificationSerializer',  # ADICIONAR AQUI TAMBÉM
]
