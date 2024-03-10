
import time
import pulsar
import threading
from flask import Flask
from entrypoints.api_rest import api_rest_blueprint
import pulsar

app = Flask(__name__)

app.register_blueprint(api_rest_blueprint)

def consumer_app():
    client = pulsar.Client('pulsar://localhost:6650')
    subscription_name = 'listener-data-audit-subscription-app'
    topic = 'persistent://public/default/comando-data-audit-topic'
    consumer = client.subscribe(topic, subscription_name)

    try:
        while True:
            msg = consumer.receive()
            print("Recibido mensaje: '{}'".format(msg.data().decode('utf-8')))
            consumer.acknowledge(msg)
            producer_data_audit = client.create_producer('persistent://public/default/evento-data-audit-topic')
            producer_data_audit.send(msg.data())
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
