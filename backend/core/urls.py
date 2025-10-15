from django.contrib import admin # Necessário para o painel Admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views # Assumindo que seu aplicativo se chama 'api'

# Cria um router e registra seus ViewSets
router = DefaultRouter()

# === Rotas das Dimensões ===
router.register(r'users', views.DimUserViewSet)
router.register(r'uos', views.DimUOViewSet)
router.register(r'cargos', views.DimCargoViewSet)
router.register(r'locais', views.DimLocalAtividadeViewSet)
router.register(r'regimes', views.DimRegimeTrabalhoViewSet)
router.register(r'tipos_req', views.DimTipoRequerimentoViewSet)
router.register(r'riscos', views.DimRiskViewSet)

# === Rota do Fato ===
router.register(r'requerimentos', views.FactRequerimentoViewSet)

# Configura as URLs
urlpatterns = [
    # ROTA CORRIGIDA: Adiciona o painel de administração
    path('admin/', admin.site.urls), 
    
    # Rota da API
    path('api/', include(router.urls)),
]
