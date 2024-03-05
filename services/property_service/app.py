import pulsar

from flask import Flask
from entrypoints.rest.api_rest import app

client = pulsar.Client('pulsar://localhost:6650')

producer = client.create_producer('My-Topic')

for i in range(10):
    producer.send(('Hello-%d' % i).encode('utf-8'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=8080, debug=True)