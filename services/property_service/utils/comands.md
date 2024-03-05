# Comandos útiles

## Para Crear el env

python -m venv venv 

## Para Activar el env

.\venv\Scripts\Activate.ps1 (Windows)
source venv/bin/activate (MacOs)

## Para instalar dependencias

pip install -r requirements.txt

## Para iniciar la app

python flask run
ó
flask run

## Instalar una dependencia

pip install python-dotenv
pip install psycopg2

## Actualizar el archivo de dependencias después de instalar una dependencia

pip freeze > requirements.txt

## Para ejecutar pulsar (cd services/pulsar)

docker compose up -d

## Eliminar todos los containers de docker

docker rm -f $(docker ps -aq)

## Crear topico 
./bin/pulsar-admin topics create "persistent://public/default/comando-propiedades-topic"


## Consumir topico
./bin/pulsar-client consume -s "sub-datos" public/default/comando-propiedades-topic -n 0