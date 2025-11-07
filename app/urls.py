from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
# Importar views de autenticação do Django Rest Framework
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# ATENÇÃO: Adicionado o FavoriteViewSet na importação
from core.views import (
    UserViewSet, ClienteViewSet, FuncionarioViewSet,
    ReservaViewSet, GeneroViewSet, MidiaViewSet,
    LocacaoViewSet, LocacaoMidiaViewSet, PagamentoViewSet,
    FavoriteViewSet,  # <-- FAVORITE VIEWSET ADICIONADO AQUI
)

# -----------------------------------------------------------
# PONTO CRÍTICO: DEFINIÇÃO DO ROUTER ANTES DO USO!
router = DefaultRouter() 
# -----------------------------------------------------------

# Rotas
router.register(r'usuarios', UserViewSet, basename='usuarios')

# ROTAS DA MINHA LISTA / FAVORITOS
# Rota para /api/favorites/ (Acesso GET, POST e DELETE por ID)
# O basename é importante porque o ViewSet não usa o nome do modelo diretamente.
router.register(r'favorites', FavoriteViewSet, basename='favorites') # <-- REGISTRO ADICIONADO

router.register(r'clientes', ClienteViewSet)
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'generos', GeneroViewSet)
router.register(r'midias', MidiaViewSet)
router.register(r'locacoes', LocacaoViewSet)
router.register(r'locacoes-midias', LocacaoMidiaViewSet)
router.register(r'pagamentos', PagamentoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),

    # API
    path('api/', include(router.urls)),
    
    # --- ROTA DE REGISTRO MANUAL PARA O FRONT-END ---
    # Liga o POST para /api/auth/register/ à ação 'create' (registro) do UserViewSet
    path(
        'api/auth/register/', 
        UserViewSet.as_view({'post': 'create'}), 
        name='user-register'
    ),
    # ------------------------------------------------

    # Rotas de autenticação (JWT)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]