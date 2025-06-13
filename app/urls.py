from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from core.views import (
    UserViewSet, ClienteViewSet, FuncionarioViewSet,
    ReservaViewSet, GeneroViewSet, MidiaViewSet,
    LocacaoViewSet, LocacaoMidiaViewSet, PagamentoViewSet
)


router = DefaultRouter()

# Rotas
router.register(r'usuarios', UserViewSet, basename='usuarios')
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
]
