from rest_framework import serializers
from .models import Cliente, Producto, CabeceraVenta, DetalleVenta

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['valor_producto', 'iva_calculado', 'producto','cabecera_venta']

class DetalleVentaSerializer_sin_cabecera_venta(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['valor_producto', 'iva_calculado', 'producto']

class CabeceraVentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer_sin_cabecera_venta(many=True)
    
    class Meta:
        model = CabeceraVenta
        fields = ['id', 'consecutivo', 'fecha', 'cliente', 'total_venta', 'detalles']
        
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        cabecera_venta = CabeceraVenta.objects.create(**validated_data)
        for detalle_data in detalles_data:
            DetalleVenta.objects.create(cabecera_venta=cabecera_venta, **detalle_data)
        return cabecera_venta
