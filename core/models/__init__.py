from .user import User
from .cliente import Cliente
from .funcionario import Funcionario
from .genero import Genero
from .midia import Midia 
from .reserva import Reserva
from .locacao import Locacao # Importa apenas Locacao (presumindo que LocacaoMidia foi removida deste arquivo)
from .locacao_midia import LocacaoMidia # Importa LocacaoMidia de um arquivo dedicado
from .pagamento import Pagamento
from .favorite import Favorite # NOVO MODELO FAVORITE

__all__ = [
    "User", "Cliente", "Funcionario", 
    "Genero", "Midia", "Reserva", 
    "Locacao", "LocacaoMidia", "Pagamento",
    "Favorite" 
]