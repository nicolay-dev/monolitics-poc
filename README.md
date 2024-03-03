# POC

## Objetivo

POC de la arquitectura de solución que su grupo está proponiendo. Dado que su arquitectura debe satisfacer la visión del negocio, no olvidé que su experimentación debe probar que la arquitectura propuesta nos va a ayudar a escalar el negocio a nivel global.

## TODO:

## Refinar y elegir los tres escenarios de calidad que vamos a utilizar con base en los comentarios de la entrega anterior

Los estudiantes diseñaron e implementaron 3 microservicios para satisfacer 3 de los escenarios de calidad definidos en la entrega pasada

*Escenarios:*
*Escenario 1:* Tiempo de respuesta en el servicio de *Propiedades*  TODO:  Nico

*Escenario 4:* Agregar soporte para un nuevo mercado con reglas de negocio y terminología local. !! *(Propiedades, DataAdapter)* TODO: JuanCa

*Escenario 8:* Mantener la consistencia de datos entre microservicios relacionados. !! *DataAudit*  TODO: Luis

// Tentativo:
*Escenario nuevo?* donde se identifique la necesidad de escalar ciertos microservicio con alta demanda  (Rendimiento - cuello de botella) para el caso se utiliza el servicio de *DataAudit*

*Corporativo*

## Desarrollo de como mínimo 3 microservicios con comunicación basada en eventos y comandos

(Sacar un microservicio genérico que aplique y replicarlos dos veces para el total de tres microservicios)

Cada micro debe estar por capas (cebolla) (Repositorios, lógica, enrutamiento, objetovalor...)

## La comunicación de todos los microservicios se hace por medio de comandos y eventos (PULSAR)

Pulsar debe ser configurado ya sea en la infrastructura (AWS o GCP (Como Pub/Sub) o como un componente aparte)

(La única excepción es la ejecución de queries síncronos, donde puede ser usado un protocolo como HTTP o gRPC.)

## Usar Apache Pulsar como broker de eventos

(Para la propagación de comandos y eventos, el equipo configuró, desplegó y uso un cluster en Apache Pulsar)

## Se justifica correctamente los tipos de eventos a utilizar (integración o carga de estado). Ello incluye la definición de los esquemas y evolución de los mismos (Documentar)

## Definir, justificar e implementar alguna de las topologías para la administración de datos descentralizada o híbrida

## Definir e implementar un modelo *CRUD* o Event Sourcing en la capa de datos en al menos 3 de los servicios

Nota:
DEBIZIUM: Tiene tabla de transacciones (Manejado por estado) (EventSourcing)

## Documentar con la descripción de actividades realizada por cada miembro

## Desplegar en una plataforma de preferencia

## El código debe encontrarse en un software de control de versionamiento como Github

[Repo]<https://github.com/nicolay-dev/monolitics-poc>

## Grabar video

## Deben ser claros los principios de DDD en el diseño: agregaciones, contextos acotados, inversión de dependencias, capas, etc

Refinamiento de los escenarios
Construcción de los micros - La comunicación BD
configurar en cada micro la comunicación por comandos y eventos
Construir Componente pulsar
Despliegue
