# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.views import View
# from lxml import etree
# from ..models import Cliente, Producto, CabeceraVenta, DetalleVenta

# class SOAPService(View):
#     """
#     Servicio SOAP para gestionar clientes, productos y ventas.

#     Endpoints:
#     - /soap/: Maneja todas las operaciones SOAP.
#     """

#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         """
#         Maneja las solicitudes SOAP POST.

#         Operaciones soportadas:
#         - CreateCliente: Crea un nuevo cliente.
#         - CreateProducto: Crea un nuevo producto.
#         - CreateVenta: Crea una nueva venta.
#         - GetClientes: Obtiene la lista de clientes.

#         Ejemplo de solicitud SOAP para CreateCliente:
#         <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://example.com/soap/">
#             <soapenv:Header/>
#             <soapenv:Body>
#                 <soap:CreateCliente>
#                     <cedula>123456</cedula>
#                     <nombre>John Doe</nombre>
#                     <direccion>Calle Falsa 123</direccion>
#                     <telefono>1234567890</telefono>
#                     <email>johndoe@example.com</email>
#                 </soap:CreateCliente>
#             </soapenv:Body>
#         </soapenv:Envelope>
#         """
#         try:
#             xml_request = request.body
#             response = self.handle_request(xml_request)
#             return HttpResponse(response, content_type="text/xml")
#         except Exception as e:
#             return HttpResponse(str(e), status=500)

#     def handle_request(self, xml_request):
#         envelope = etree.fromstring(xml_request)
#         body = envelope.find('{http://schemas.xmlsoap.org/soap/envelope/}Body')
        
#         if body.find('{http://example.com/soap/}CreateCliente') is not None:
#             return self.create_cliente(body)
#         elif body.find('{http://example.com/soap/}CreateProducto') is not None:
#             return self.create_producto(body)
#         elif body.find('{http://example.com/soap/}CreateVenta') is not None:
#             return self.create_venta(body)
#         elif body.find('{http://example.com/soap/}GetClientes') is not None:
#             return self.get_clientes()
#         else:
#             raise ValueError("Invalid SOAP operation")

#     def create_cliente(self, body):
#         data = body.find('{http://example.com/soap/}CreateCliente')
#         cedula = data.find('cedula').text
#         nombre = data.find('nombre').text
#         direccion = data.find('direccion').text
#         telefono = data.find('telefono').text
#         email = data.find('email').text

#         Cliente.objects.create(
#             cedula=cedula,
#             nombre=nombre,
#             direccion=direccion,
#             telefono=telefono,
#             email=email
#         )
        
#         response = etree.Element('{http://schemas.xmlsoap.org/soap/envelope/}Envelope')
#         body = etree.SubElement(response, '{http://schemas.xmlsoap.org/soap/envelope/}Body')
#         result = etree.SubElement(body, 'CreateClienteResponse', xmlns="http://example.com/soap/")
#         result.text = "Cliente creado exitosamente"
        
#         return etree.tostring(response)

#     def create_producto(self, body):
#         data = body.find('{http://example.com/soap/}CreateProducto')
#         codigo = data.find('codigo').text
#         nombre = data.find('nombre').text
#         valor_venta = float(data.find('valor_venta').text)
#         maneja_iva = data.find('maneja_iva').text == 'true'
#         porcentaje_iva = float(data.find('porcentaje_iva').text)

#         Producto.objects.create(
#             codigo=codigo,
#             nombre=nombre,
#             valor_venta=valor_venta,
#             maneja_iva=maneja_iva,
#             porcentaje_iva=porcentaje_iva
#         )
        
#         response = etree.Element('{http://schemas.xmlsoap.org/soap/envelope/}Envelope')
#         body = etree.SubElement(response, '{http://schemas.xmlsoap.org/soap/envelope/}Body')
#         result = etree.SubElement(body, 'CreateProductoResponse', xmlns="http://example.com/soap/")
#         result.text = "Producto creado exitosamente"
        
#         return etree.tostring(response)

#     def create_venta(self, body):
#         data = body.find('{http://example.com/soap/}CreateVenta')
#         consecutivo = data.find('consecutivo').text
#         fecha = data.find('fecha').text
#         cliente_data = data.find('cliente')
#         cliente = Cliente.objects.get(cedula=cliente_data.find('cedula').text)
#         total_venta = float(data.find('total_venta').text)

#         cabecera = CabeceraVenta.objects.create(
#             consecutivo=consecutivo,
#             fecha=fecha,
#             cliente=cliente,
#             total_venta=total_venta
#         )

#         for detalle_data in data.findall('detalles'):
#             producto_data = detalle_data.find('producto')
#             producto = Producto.objects.get(codigo=producto_data.find('codigo').text)
#             valor_producto = float(detalle_data.find('valor_producto').text)
#             iva_calculado = float(detalle_data.find('iva_calculado').text)

#             DetalleVenta.objects.create(
#                 cabecera_venta=cabecera,
#                 producto=producto,
#                 valor_producto=valor_producto,
#                 iva_calculado=iva_calculado
#             )

#         response = etree.Element('{http://schemas.xmlsoap.org/soap/envelope/}Envelope')
#         body = etree.SubElement(response, '{http://schemas.xmlsoap.org/soap/envelope/}Body')
#         result = etree.SubElement(body, 'CreateVentaResponse', xmlns="http://example.com/soap/")
#         result.text = "Venta creada exitosamente"
        
#         return etree.tostring(response)

#     def get_clientes(self):
#         clientes = Cliente.objects.all()
#         response = etree.Element('{http://schemas.xmlsoap.org/soap/envelope/}Envelope')
#         body = etree.SubElement(response, '{http://schemas.xmlsoap.org/soap/envelope/}Body')
#         result = etree.SubElement(body, 'GetClientesResponse', xmlns="http://example.com/soap/")
        
#         for cliente in clientes:
#             cliente_element = etree.SubElement(result, 'Cliente')
#             cedula = etree.SubElement(cliente_element, 'cedula')
#             cedula.text = cliente.cedula
#             nombre = etree.SubElement(cliente_element, 'nombre')
#             nombre.text = cliente.nombre
#             direccion = etree.SubElement(cliente_element, 'direccion')
#             direccion.text = cliente.direccion
#             telefono = etree.SubElement(cliente_element, 'telefono')
#             telefono.text = cliente.telefono
#             email = etree.SubElement(cliente_element, 'email')
#             email.text = cliente.email

#         return etree.tostring(response)
