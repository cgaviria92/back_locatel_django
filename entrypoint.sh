# #!/bin/sh

# # Ejecutar las migraciones
# python manage.py migrate

# # Crear el superusuario si no existe
# python manage.py shell <<EOF
# from django.contrib.auth.models import User
# from django.conf import settings

# if not User.objects.filter(username=settings.SUPERUSER_USERNAME).exists():
#     User.objects.create_superuser(
#         username=settings.SUPERUSER_USERNAME,
#         email=settings.SUPERUSER_EMAIL,
#         password=settings.SUPERUSER_PASSWORD
#     )
#     print("Superuser created successfully")
# else:
#     print("Superuser already exists")
# EOF

# # Ejecutar el servidor de desarrollo de Django
# exec "$@"
