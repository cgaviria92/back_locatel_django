from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Cliente, Producto, CabeceraVenta, DetalleVenta
from .serializers import ClienteSerializer, ProductoSerializer, CabeceraVentaSerializer, DetalleVentaSerializer
from django_filters.rest_framework import DjangoFilterBackend

class ClienteViewSet(views.APIView):# definir vistas basadas en clases
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ClienteSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        queryset = Cliente.objects.all()
        serializer = ClienteSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ClienteSerializer, responses={201: ClienteSerializer})
    def post(self, request, *args, **kwargs):
        serializer = ClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductoViewSet(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: ProductoSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        queryset = Producto.objects.all()
        serializer = ProductoSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProductoSerializer, responses={201: ProductoSerializer})
    def post(self, request, *args, **kwargs):
        serializer = ProductoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CabeceraVentaViewSet(views.APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fecha']

    @swagger_auto_schema(responses={200: CabeceraVentaSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        queryset = CabeceraVenta.objects.all()
        queryset = self.filter_queryset(queryset)
        serializer = CabeceraVentaSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CabeceraVentaSerializer, responses={201: CabeceraVentaSerializer})
    def post(self, request, *args, **kwargs):
        serializer = CabeceraVentaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

class DetalleVentaViewSet(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: DetalleVentaSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        queryset = DetalleVenta.objects.all()
        serializer = DetalleVentaSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DetalleVentaSerializer, responses={201: DetalleVentaSerializer})
    def post(self, request, *args, **kwargs):
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
