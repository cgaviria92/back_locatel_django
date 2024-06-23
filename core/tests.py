from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Cliente, Producto, CabeceraVenta, DetalleVenta

class ClienteModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            cedula="123456",
            nombre="John Doe",
            direccion="Calle Falsa 123",
            telefono="1234567890",
            email="johndoe@example.com"
        )

    def test_cliente_creation(self):
        self.assertEqual(self.cliente.cedula, "123456")
        self.assertEqual(self.cliente.nombre, "John Doe")
        self.assertEqual(self.cliente.direccion, "Calle Falsa 123")
        self.assertEqual(self.cliente.telefono, "1234567890")
        self.assertEqual(self.cliente.email, "johndoe@example.com")

class ProductoModelTest(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            codigo="P001",
            nombre="Shampoo",
            valor_venta=100.0,
            maneja_iva=True,
            porcentaje_iva=19.0
        )

    def test_producto_creation(self):
        self.assertEqual(self.producto.codigo, "P001")
        self.assertEqual(self.producto.nombre, "Shampoo")
        self.assertEqual(self.producto.valor_venta, 100.0)
        self.assertEqual(self.producto.maneja_iva, True)
        self.assertEqual(self.producto.porcentaje_iva, 19.0)

class APITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.client = APIClient()
        self.token = self.get_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def get_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'admin',
            'password': 'admin'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_create_cliente(self):
        url = reverse('cliente-list')
        data = {
            "cedula": "123456",
            "nombre": "John Doe",
            "direccion": "Calle Falsa 123",
            "telefono": "1234567890",
            "email": "johndoe@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 1)
        self.assertEqual(Cliente.objects.get().nombre, 'John Doe')

    def test_create_producto(self):
        url = reverse('producto-list')
        data = {
            "codigo": "P001",
            "nombre": "Shampoo",
            "valor_venta": 100.0,
            "maneja_iva": True,
            "porcentaje_iva": 19.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(Producto.objects.get().nombre, 'Shampoo')

    def test_create_cabecera_venta(self):
        cliente = Cliente.objects.create(
            cedula="123456",
            nombre="John Doe",
            direccion="Calle Falsa 123",
            telefono="1234567890",
            email="johndoe@example.com"
        )
        producto = Producto.objects.create(
            codigo="P001",
            nombre="Shampoo",
            valor_venta=100.0,
            maneja_iva=True,
            porcentaje_iva=19.0
        )
        url = reverse('cabeceraventa-list')
        data = {
            "consecutivo": "CV001",
            "fecha": "2024-06-22",
            "cliente": cliente.id,
            "total_venta": 119.0,
            "detalles": [
                {
                    "producto": producto.id,
                    "valor_producto": 100.0,
                    "iva_calculado": 19.0
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CabeceraVenta.objects.count(), 1)
        self.assertEqual(CabeceraVenta.objects.get().consecutivo, 'CV001')

    def test_get_clientes(self):
        Cliente.objects.create(
            cedula="123456",
            nombre="John Doe",
            direccion="Calle Falsa 123",
            telefono="1234567890",
            email="johndoe@example.com"
        )
        url = reverse('cliente-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_productos(self):
        Producto.objects.create(
            codigo="P001",
            nombre="Shampoo",
            valor_venta=100.0,
            maneja_iva=True,
            porcentaje_iva=19.0
        )
        url = reverse('producto-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
