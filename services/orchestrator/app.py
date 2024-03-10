from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from dotenv import load_dotenv
from os import getenv
from modelos import db, Transaction
import pulsar
import threading

def set_env():
    load_dotenv()
    global DATABASE_URL
    DATABASE_URL = getenv("DATABASE_URL")
    global JWT_SECRET_KEY
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    
set_env()

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
application.config['PROPAGATE_EXCEPTIONS'] = True
app_context = application.app_context()
app_context.push()
db.init_app(application)
db.create_all()

api = Api(application)
jwt = JWTManager(application)

client = pulsar.Client('pulsar://localhost:6650')
topico_comando_property = 'persistent://public/default/comando-property-topic'  
topico_evento_property = 'persistent://public/default/evento-property-topic'

topico_comando_data_adapter = 'persistent://public/default/comando-data-adapter-topic'
topico_evento_data_adapter = 'persistent://public/default/evento-data-adapter-topic'

##Suscriptores
suscriptor_property_evento = 'listener-property-event-subscription'
consumer = client.subscribe(topico_evento_property, suscriptor_property_evento)

##Productores
producer_data_adapter = client.create_producer(topico_comando_data_adapter)


def consumer_app():
    try:
        while True:
            msg = consumer.receive()
            data = msg.data().decode('utf-8')
            print("Recibido mensaje: '{}'".format(data))
            consumer.acknowledge(msg)
            producer_data_adapter.send(data.encode('utf-8'))
            transaction_db(data)
    except Exception as e:
        print(e)
    finally:
        print('Fin escuchando...')
        client.close()

def transaction_db(data):
    data_dict = eval(data)

    with application.app_context():  # Usamos el contexto de la aplicación aquí
        new_transaction = Transaction(
            uuid=data_dict.get('transaction_id'),
            fact=data_dict.get('method'),
            resource_tp=topico_evento_property,
            destination_tp=topico_comando_data_adapter,
            status='OK'
        )
        db.session.add(new_transaction)
        try:
            db.session.commit()
            print('Transacción guardada')
        except Exception as e:
            print(f'Error al guardar la transacción: {e}')
            db.session.rollback()
        
        

if __name__ == 'app':
    threading.Thread(target=consumer_app, daemon=True).start()


