from django.contrib import admin
from .models import Cliente, Producto, CabeceraVenta, DetalleVenta
# Register your models here.
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(CabeceraVenta)
admin.site.register(DetalleVenta)