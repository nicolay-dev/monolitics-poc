from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from dotenv import load_dotenv
from os import getenv
from modelos import db, Transaction
import pulsar
import threading
import random

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

#Topicos comando
topico_comando_property = 'persistent://public/default/comando-property-topic' 
topico_comando_data_adapter = 'persistent://public/default/comando-data-adapter-topic'
topico_comando_data_audit = 'persistent://public/default/comando-data-audit-topic'

#Topicos evento
topico_evento_property = 'persistent://public/default/evento-property-topic'
topico_evento_data_adapter = 'persistent://public/default/evento-data-adapter-topic'
topico_evento_data_audit = 'persistent://public/default/evento-data-audit-topic'

##Suscriptores
suscriptor_property_evento = 'listener-property-event-subscription-orhcestrator'
suscriptor_data_adapter_evento = 'listener-data-adapter-event-subscription-orhcestrator'
suscriptor_data_audit_evento = 'listener-data-audit-event-subscription-orhcestrator'


##Productores
producer_property = client.create_producer(topico_comando_property)
producer_data_adapter = client.create_producer(topico_comando_data_adapter)
producer_data_audit = client.create_producer(topico_comando_data_audit)


def consumer_app(topico_evento, topico_comando, suscriptor, producer):
    try:
        while True:
            consumer = client.subscribe(topico_evento, suscriptor)
            msg = consumer.receive()
            data = msg.data().decode('utf-8')
            print("Mensaje recibido del topico: " + topico_evento)
            print("Recibido mensaje: '{}'".format(data))
            consumer.acknowledge(msg)
            producer.send(data.encode('utf-8'))
            print("Mensaje enviado al topico: " + topico_comando)
            transaction_db(data, topico_evento, topico_comando)
            print("Transacción guardada")
            consumer.close()
    except Exception as e:
        print(e)

def transaction_db(data, topico_evento, topico_comando):
    data_dict = eval(data)
    with application.app_context():  # Usamos el contexto de la aplicación aquí
        new_transaction = Transaction(
            uuid=data_dict.get('transaction_id'),
            fact=data_dict.get('method'),
            resource_tp=topico_evento,
            destination_tp=topico_comando,
            status='OK'
        )
        db.session.add(new_transaction)
        try:
            db.session.commit()
            print('Transacción guardada')
        except Exception as e:
            print(f'Error al guardar la transacción: {e}')
            db.session.rollback()


def task_1 ():
    consumer_app(topico_evento_property, topico_comando_data_adapter, suscriptor_property_evento, producer_data_adapter)
    
def task_2 ():
    consumer_app(topico_evento_data_adapter, topico_comando_data_audit, suscriptor_data_adapter_evento, producer_data_audit)

def task_complete_transaction():
    try:
        while True:
            consumer = client.subscribe(topico_evento_data_audit, suscriptor_data_audit_evento)
            msg = consumer.receive()
            data = msg.data().decode('utf-8')
            consumer.acknowledge(msg)
            data_dict = eval(data)
            status = 'OK' if random.random() < 0.5 else 'FAIL'
            print("Mensaje recibido del topico: " + topico_evento_data_audit)
            print("Estado de la transacción: " + status)
            if status == 'OK':
                with application.app_context():
                    new_transaction = Transaction(
                        uuid=data_dict.get('transaction_id'),
                        fact='Transaccion completada',
                        resource_tp=topico_evento_data_audit,
                        destination_tp= 'Finalizado',
                        status=status
                    )
                    db.session.add(new_transaction)
                    try:
                        db.session.commit()
                        print('Transacción guardada')
                    except Exception as e:
                        print(f'Error al guardar la transacción: {e}')
                        db.session.rollback()
            if status == 'FAIL':
                with application.app_context():
                    rollback_1 = Transaction(
                        uuid=data_dict.get('transaction_id'),
                        fact='Rollback de transacción data audit',
                        resource_tp=topico_comando_data_audit,
                        destination_tp= 'Finalizado',
                        status='Complete'
                    )
                    db.session.add(rollback_1)
                    try:
                        db.session.commit()
                        print('Transacción guardada')
                    except Exception as e:
                        print(f'Error al guardar la transacción: {e}')
                        db.session.rollback()
                    
                    rollback_2 = Transaction(
                        uuid=data_dict.get('transaction_id'),
                        fact='Rollback de transacción data adapter',
                        resource_tp=topico_comando_data_adapter,
                        destination_tp= 'Finalizado',
                        status='Complete'
                    )
                    db.session.add(rollback_2)
                    try:
                        db.session.commit()
                        print('Transacción guardada')
                    except Exception as e:
                        print(f'Error al guardar la transacción: {e}')
                        db.session.rollback()
                        

            

    except Exception as e:
        print(e)
         
if __name__ == 'app':
    threading.Thread(target=task_1, daemon=True).start()
    threading.Thread(target=task_2, daemon=True).start()
    threading.Thread(target=task_complete_transaction, daemon=True).start()


