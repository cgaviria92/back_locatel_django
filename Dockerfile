# Usar la imagen base oficial de Python 3.12.4
FROM python:3.12.4

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar los archivos de requisitos al directorio de trabajo
COPY requirements.txt /app/

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del codigo de la aplicación al directorio de trabajo
COPY . /app/

# Ejecutar las migraciones
#RUN python manage.py migrate

# Copiar el script de inicialización
#COPY entrypoint.sh /app/

# Asignar permisos de ejecución al script
#RUN chmod +x /app/entrypoint.sh

# Exponer el puerto en el que Django ejecutará la aplicación (por defecto 8000)
EXPOSE 8000

# Establecer el script de inicialización como punto de entrada
#ENTRYPOINT ["/app/entrypoint.sh"]
