FROM python:3.11.0

# Crea el directorio de trabajo de la aplicación
WORKDIR /app

# Copia los archivos requeridos de tu proyecto a la imagen de Docker
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Establece el puerto que expondrá el contenedor
EXPOSE 8000

# Ejecuta el comando que inicia la aplicación
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
