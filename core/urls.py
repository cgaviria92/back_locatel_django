from django.urls import include, path
from .views import ClienteViewSet, ProductoViewSet, CabeceraVentaViewSet, DetalleVentaViewSet

urlpatterns = [
    path('clientes/', ClienteViewSet.as_view(), name='cliente-list-create'),
    path('productos/', ProductoViewSet.as_view(), name='producto-list-create'),
    path('cabecera-ventas/', CabeceraVentaViewSet.as_view(), name='cabecera-venta-list-create'),
    path('detalle-ventas/', DetalleVentaViewSet.as_view(), name='detalle-venta-list-create'),
    path('api-auth/', include('rest_framework.urls')),
]
