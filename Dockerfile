# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Evita buffer de Python
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV DJANGO_SETTINGS_MODULE=ministerio_educacion.settings

# Directorio de trabajo
WORKDIR /app

# Dependencias necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el proyecto
COPY . /app

# ❌ NO correr collectstatic porque vos ya tenés la carpeta staticfiles
# RUN python manage.py collectstatic --no-input

# Ejecutar migraciones + levantar Gunicorn al iniciar el contenedor
CMD ["sh", "-c", "python manage.py migrate --no-input && gunicorn ministerio_educacion.wsgi:application --bind 0.0.0.0:$PORT"]
