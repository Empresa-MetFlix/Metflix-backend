from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

# Importar views
from core.views import (
    UserViewSet, 
    ClienteViewSet, 
    FuncionarioViewSet,
    ReservaViewSet, 
    GeneroViewSet, 
    MidiaViewSet,
    LocacaoViewSet, 
    LocacaoMidiaViewSet, 
    PagamentoViewSet,
    FavoriteViewSet,
)

# Importar custom token view
from core.views.token import CustomTokenObtainPairView

# -----------------------------------------------------------
# ROUTER CONFIGURATION
# -----------------------------------------------------------
router = DefaultRouter()

# Rotas de usuários
router.register(r'usuarios', UserViewSet, basename='usuarios')

# Rotas de favoritos (Minha Lista)
router.register(r'favorites', FavoriteViewSet, basename='favorites')

# Rotas de clientes e funcionários
router.register(r'clientes', ClienteViewSet)
router.register(r'funcionarios', FuncionarioViewSet)

# Rotas de reservas
router.register(r'reservas', ReservaViewSet)

# Rotas de gêneros e mídias
router.register(r'generos', GeneroViewSet)
router.register(r'midias', MidiaViewSet)

# Rotas de locações
router.register(r'locacoes', LocacaoViewSet)
router.register(r'locacoes-midias', LocacaoMidiaViewSet)

# Rotas de pagamentos
router.register(r'pagamentos', PagamentoViewSet)

# -----------------------------------------------------------
# URL PATTERNS
# -----------------------------------------------------------
urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # OpenAPI 3 / Swagger / Redoc
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
    
    # API Router (todas as rotas registradas)
    path('api/', include(router.urls)),
    
    # --- AUTENTICAÇÃO ---
    # Rota de registro manual (POST /api/auth/register/)
    path(
        'api/auth/register/',
        UserViewSet.as_view({'post': 'create'}),
        name='user-register'
    ),
    
    # Rota de login JWT customizada (POST /api/token/)
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Rota de refresh token (POST /api/token/refresh/)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Rota de informações do usuário logado (GET /api/usuarios/me/)
    # Já está coberta pelo router via @action no UserViewSet
]
