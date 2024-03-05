import pulsar

client = pulsar.Client('pulsar://localhost:6650')

subscription_name = 'listener-propiedades-subscription'
topic = 'persistent://public/default/comando-data-adapter-topic'

consumer = client.subscribe(topic, subscription_name)

try:
    while True:
        msg = consumer.receive()
        print("Recibido mensaje: '{}'".format(msg.data().decode('utf-8')))
        # Aquí podrías procesar el mensaje como necesites
        consumer.acknowledge(msg)
except Exception as e:
    print(e)
finally:
    client.close()