from .user import UserSerializer
from .cliente import ClienteSerializer
from .funcionario import FuncionarioSerializer
from .genero import GeneroSerializer
from .midia import MidiaSerializer, MidiaDetailSerializer
from .reserva import ReservaSerializer
from .locacao import LocacaoSerializer
# from .locacao_midia import LocacaoMidiaSerializer
from .pagamento import PagamentoSerializer
from .favorite import FavoriteSerializer # <-- DEVE ESTAR AQUI

__all__ = [
    "UserSerializer", "ClienteSerializer", "FuncionarioSerializer", 
    "GeneroSerializer", "MidiaSerializer", "MidiaDetailSerializer", 
    "ReservaSerializer", "LocacaoSerializer", "LocacaoMidiaSerializer", 
    "PagamentoSerializer", "FavoriteSerializer" # <-- E AQUI
]