# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece variables de entorno necesarias
ENV PYTHONUNBUFFERED 1
ENV PORT=8080 
# Nombre de la carpeta principal de configuracion de Django
ENV DJANGO_SETTINGS_MODULE=ministerio_educacion.settings 

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de dependencia e instala
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia todo el código del proyecto al contenedor
COPY . /app

# Recolección de archivos estáticos para servir el CSS/JS
RUN python manage.py collectstatic --no-input

# Comando que se ejecuta al iniciar el contenedor (usando Gunicorn)
# El puerto se toma de la variable ENV PORT=8080
CMD exec gunicorn evaluaciones_educativas.wsgi:application --bind :$PORT