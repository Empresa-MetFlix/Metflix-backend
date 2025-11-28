from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from core.views import (
    UserViewSet,
    ClienteViewSet,
    FuncionarioViewSet,
    MidiaViewSet,
    GeneroViewSet,
    LocacaoViewSet,
    LocacaoMidiaViewSet,
    PagamentoViewSet,
    ReservaViewSet,
    FavoriteViewSet,
    NotificationViewSet,
    CustomTokenObtainPairView,
    register_view,
)

from core.views.profile import profiles_list, profile_detail

# Configurar router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'clientes', ClienteViewSet)
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'midias', MidiaViewSet)
router.register(r'generos', GeneroViewSet)
router.register(r'locacoes', LocacaoViewSet)
router.register(r'locacoes-midias', LocacaoMidiaViewSet)
router.register(r'pagamentos', PagamentoViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticação JWT
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', register_view, name='register'),
    
    # Profiles (✅ CORRIGIDO)
    path('api/profiles/', profiles_list, name='profiles-list'),
    path('api/profiles/<int:pk>/', profile_detail, name='profile-detail'),
    
    # Router padrão
    path('api/', include(router.urls)),
]
