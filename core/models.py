from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    valor_venta = models.DecimalField(max_digits=10, decimal_places=2)
    maneja_iva = models.BooleanField(default=False)
    porcentaje_iva = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return self.nombre

class CabeceraVenta(models.Model):
    consecutivo = models.CharField(max_length=20, unique=True, blank=True)
    fecha = models.DateField(default=timezone.now)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.consecutivo:
            max_id = CabeceraVenta.objects.all().aggregate(models.Max('id'))['id__max']
            self.consecutivo = f'CV-{max_id + 1 if max_id else 1:05d}'
        super(CabeceraVenta, self).save(*args, **kwargs)

    def __str__(self):
        return self.consecutivo

class DetalleVenta(models.Model):
    valor_producto = models.DecimalField(max_digits=10, decimal_places=2)
    iva_calculado = models.DecimalField(max_digits=10, decimal_places=2)
    cabecera_venta = models.ForeignKey(CabeceraVenta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cabecera_venta.consecutivo} - {self.producto.nombre}'
