#!/bin/bash

# Iniciar Apache Pulsar en modo standalone
bin/pulsar standalone &

# Esperar a que Pulsar esté completamente arriba
sleep 60  # Ajusta este tiempo si es necesario

# Ejecutar el conector Debezium
/bin/pulsar-admin source localrun --source-config-file /pulsar/conf/debezium-postgres-source-config.yaml --destination-topic-name debezium-postgres-topic

# Mantener el contenedor en ejecución
tail -f /dev/null
