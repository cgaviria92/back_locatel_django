# Proyecto de Ventas

Este es un proyecto de ventas básico desarrollado con Django y Django REST Framework. El proyecto incluye funcionalidades para la gestión de clientes, productos, y ventas, así como autenticación basada en tokens JWT y una interfaz API documentada con Swagger.
# usuario por defecto
### user: `admin` password: `admin`

## Endpoints Principales

- `api/token/`: Obtener token de acceso y refresco.
- `api/token/refresh/`: Refrescar token de acceso.
- `api/clientes/`: Gestión de clientes.
- `api/productos/`: Gestión de productos.
- `api/cabecera-ventas/`: Gestión de cabeceras de ventas.
- `api/detalle-ventas/`: Gestión de detalles de ventas.
- `swagger/`: Documentación Swagger.
- `admin/`: Django admin interfaces

## Implementacion adicional
- Seguridad con token
- Encriptación de contraseña en la base de datos.
- Implementacion de cors unicamentte recibe peticiones  desde `http://localhost:4200/`

## Pruebas unitarias `pytest`


## Archivo `Dockerfile`

El archivo `Dockerfile` está configurado para instalar dependencias, aplicar migraciones y crear un superusuario automaticamente:

1. Compilar imagen del contenedor
    ```bash
    docker build -t ventas-app .
    ```
2. Desplegar en Docker
    ```bash
    docker run -p 8000:8000 ventas-app python manage.py runserver 0.0.0.0:8000
    ```
## Instalación de manera local "en tú equipo"
1. Crea un entorno virtual y activalo:

    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa: env\Scripts\activate
    ```
2. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```
3. Iniciar migraciones:

    ```bash
    python manage.py migrate
    ```
4. Inicia el servidor de desarrollo:

    ```bash
    python manage.py runserver
    ```