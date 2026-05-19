#!/bin/bash

#!/bin/bash

# 1. Limpieza estricta de contenedores y carpetas previas
docker stop samplerunning || true
docker rm samplerunning || true
rm -rf tempdir

# 2. Crear la estructura temporal
mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

# 3. Copiar los archivos base
cp sample_app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

# 4. Crear el Dockerfile con el truco para evadir el bug de los hilos
echo "FROM python:3.9-slim" > tempdir/Dockerfile
# Usamos --progress-bar off para evitar que explote por el error de hilos
echo "RUN pip install --no-cache-dir --progress-bar off flask" >> tempdir/Dockerfile
echo "COPY ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY sample_app.py /home/myapp/" >> tempdir/Dockerfile
echo "EXPOSE 5050" >> tempdir/Dockerfile
echo "CMD python /home/myapp/sample_app.py" >> tempdir/Dockerfile

# 5. Compilar la imagen de Docker
cd tempdir
docker build -t sampleapp .

# 6. Desplegar el contenedor en el puerto 8888 solicitado por la rúbrica
docker run -d -p 8888:5050 --name samplerunning sampleapp

# 7. Mostrar estado del contenedor en tiempo real
sleep 2
docker ps -a
