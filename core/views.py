from rest_framework import viewsets, status,filters
from rest_framework.response import Response
from .models import Cliente, Producto, CabeceraVenta, DetalleVenta
from .serializers import ClienteSerializer, ProductoSerializer, CabeceraVentaSerializer, DetalleVentaSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

class CabeceraVentaViewSet(viewsets.ModelViewSet):
    queryset = CabeceraVenta.objects.all()
    serializer_class = CabeceraVentaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['fecha']
    ordering_fields = ['fecha']
    ordering = ['fecha']
    permission_classes = [IsAuthenticated]

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        cabecera_venta_id = data.get('cabecera_venta')
        if not cabecera_venta_id:
            return Response({"error": "cabecera_venta is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cabecera_venta = CabeceraVenta.objects.get(id=cabecera_venta_id)
        except CabeceraVenta.DoesNotExist:
            return Response({"error": "cabecera_venta not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data['cabecera_venta'] = cabecera_venta.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


