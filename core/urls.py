from django.urls import path, include
from rest_framework.routers import DefaultRouter

#from .soap_services import SOAPService
from .views import ClienteViewSet, ProductoViewSet, CabeceraVentaViewSet, DetalleVentaViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'cabecera-ventas', CabeceraVentaViewSet)
router.register(r'detalle-ventas', DetalleVentaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
