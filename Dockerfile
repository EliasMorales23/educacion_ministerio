# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV DJANGO_SETTINGS_MODULE=ministerio_educacion.settings
# Variables para superusuario
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=eliasmorales.21@hotmail.com
ENV DJANGO_SUPERUSER_PASSWORD=42263226

# Directorio de trabajo
WORKDIR /app

# Copia dependencias e instala
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia todo el código del proyecto
COPY . /app

# Recolección de archivos estáticos
RUN python manage.py collectstatic --no-input

# Ejecuta migraciones y crea superusuario
RUN python manage.py migrate --no-input
RUN python manage.py migrate --database=Evaluacion --no-input
RUN python manage.py createsuperuser --no-input \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL

# Comando de inicio (Gunicorn)
CMD exec gunicorn ministerio_educacion.wsgi:application --bind :$PORT
