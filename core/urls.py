from django.urls import path, include
from rest_framework.routers import DefaultRouter

#from .soap_services import SOAPService
from .views import ClienteViewSet, ProductoViewSet, CabeceraVentaViewSet, DetalleVentaViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'cabecera-ventas', CabeceraVentaViewSet, basename='cabeceraventa')
router.register(r'detalle-ventas', DetalleVentaViewSet, basename='detalleventa')

urlpatterns = [
    path('', include(router.urls)),
]
