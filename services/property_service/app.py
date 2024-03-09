import time
import pulsar
import threading
from flask import Flask
from entrypoints.rest.api_rest import api_rest_blueprint

app = Flask(__name__)

app.register_blueprint(api_rest_blueprint)

def write_hello_world():
    while True:
        with open('HelloWorldThread.txt', 'a') as file:
            file.write('Hola mundo\n')
        time.sleep(1)  

def consumer_app():
    client = pulsar.Client('pulsar://localhost:6650')
    subscription_name = 'listener-propiedades-audit-subscription'
    topic = 'persistent://public/default/comando-data-adapter-topic'
    consumer = client.subscribe(topic, subscription_name)

    try:
        while True:
            msg = consumer.receive()
            print("Recibido mensaje: '{}'".format(msg.data().decode('utf-8')))
            # Procesamiento del tópico (Escribe el mensaje en un archivo)
            with open('consumer_messages.txt', 'a') as file:
                file.write(msg.data().decode('utf-8') + '\n')
            consumer.acknowledge(msg)
    except Exception as e:
        print(e)
    finally:
        print('Fin escuchando...')
        client.close()

def api_rest():
    app.run(host = '0.0.0.0', port=8080, debug=True)

if __name__ == 'app':
    threading.Thread(target=consumer_app, daemon=True).start()
    threading.Thread(target=api_rest, daemon=True).start()
    
    ## Prueba que los hilos Funcionan escribiendo en archivo 
    # threading.Thread(target=write_hello_world, daemon=True).start()
