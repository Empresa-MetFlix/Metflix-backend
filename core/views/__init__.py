from .user import UserViewSet
from .cliente import ClienteViewSet
from .funcionario import FuncionarioViewSet
from .reserva import ReservaViewSet
from .genero import GeneroViewSet
from .midia import MidiaViewSet
from .locacao import LocacaoViewSet, LocacaoMidiaViewSet
from .pagamento import PagamentoViewSet

__all__ = [
    "UserViewSet", "ClienteViewSet", "FuncionarioViewSet",
    "ReservaViewSet", "GeneroViewSet", "MidiaViewSet",
    "LocacaoViewSet", "LocacaoMidiaViewSet", "PagamentoViewSet"
]