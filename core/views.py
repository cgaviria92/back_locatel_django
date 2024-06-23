from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cliente, Producto, CabeceraVenta, DetalleVenta
from .serializers import ClienteSerializer, ProductoSerializer, CabeceraVentaSerializer, DetalleVentaSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

class ClienteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Cliente.objects.all()
        serializer = ClienteSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Producto.objects.all()
        serializer = ProductoSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ProductoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CabeceraVentaViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['fecha']
    ordering_fields = ['fecha']
    ordering = ['fecha']

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = CabeceraVenta.objects.all()
        queryset = self.filter_queryset(queryset)
        serializer = CabeceraVentaSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CabeceraVentaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class DetalleVentaViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = DetalleVenta.objects.all()
        serializer = DetalleVentaSerializer(queryset, many=True)
        return Response(serializer.data)

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
        serializer = DetalleVentaSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



#permission_classes = [IsAuthenticated]
#from rest_framework.permissions import IsAuthenticated