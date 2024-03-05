# Prueba de Concepto Apps NO Monolíticas

## Objetivo

Realizar una prueba de concepto sobre la arquitectura propuesta para satisfacer la visión del negocio de Propiedades de los Alpes, se debe probar que la arquitectura propuesta va a ayudar a escalar el negocio a nivel global.

#### Requerimientos de calidad claves identificados:

| Rendimiento | Mantenibilidad | Interoperatibilidad |
| ----------- | -------------- | ------------------- |
| Se requiere de una **experiencia de usuario fluida,  confiable y actualizada**, especialmente durante la expansión a nuevos lugares y mercados. El sistema debe poder crecer y adaptarse globalmente, evitando dificultades en el impacto de la **eficiencia operativa**, reduciendo costos y manteniendo la productividad en un nivel óptimo | Se requiere un sistema altamente **escalable, adaptable y flexible** tanto en términos tecnológicos como de recursos humanos. Esto implica una **arquitectura modular** y transparente que facilite actualizaciones, correcciones y mejoras. Además, la capacidad de realizar pruebas y depuraciones fácilmente es crucial para mantener la calidad del sistema a largo plazo. | La expansión a diferentes mercados demanda una **integración fluida con otros sistemas y servicios**, haciendo que la interoperabilidad sea crucial. El sistema debe integrarse efectivamente con sistemas existentes en cada mercado y cumplir con estándares y protocolos de comunicación. Esto aseguraría una transferencia de datos sin contratiempos entre los diversos sistemas involucrados en las operaciones comerciales e investigativas de la compañía. |

## Arquitectura planteada

Se plantea una arquitectura basada en eventos para suplir las necesidades actuales de propiedades de los alpes, dentro de las cuales se destacan:

- Expansión global a multiples mercados y regiones.
- Desacoplar la implementación monolitica actual que trae consigo diversos puntos de dolor a la hora de integrar nuevas funcionalidades y expandisrse a nuevos mercados
- Se quiere tener una arquitectura altamente escalable, modificable y extensible en la parte tecnológica pero también de recursos humanos.
- Soporte de grandes volumenes de información

![Diagrama Componente Conector](./assets/images/Diagrama%20Componente%20Conector.png)
_Diagrama 1. Componente & Conector (Punto de vista Funcional)_

El diagrama ilustra el papel central de un broker como **gestor de eventos**, permitiendo establecer una **coreografía** dinámica de los microservicios en respuesta a las actualizaciones en el flujo operativo del negocio.

Cada que se actualiza la información de las propiedades se hace una publicación sobre el topico **'UpdatePropertyInfo'** al cúal se encuentran suscritos los micorservicios de *Property y DataAudit*

### Microservicios propuestos

- **Property:** Microservicio especializado en las operaciones relacionadas con las propiedades, este almacena la información más actual de las propiedades. *(Modelo CRUD)*
- **DataAdapter:** Dado que Propiedades de los Alpes desea expandir sus operaciones a otros paises, se plantea la construcción de este microservicio encargado de crear una interfaz que sea capaz de comunicarse con las diferentes fuentes y regulaciones de cada país. De esta forma se *desacopla el dominio de Propiedad de las fuentes de información.*
- **DataAudit:** Automatiza el proceso de auditoría verificando registros que tengan un índice de confiabilidad menor a 0.8, este calculo se hace respecto a valores de *Fuente, Consistencia, Completitud*
- **FieldResearch:** Microservicio que expone un endpoint para permitir a los investigadores de campo completar información relevante de las propiedades
- **SalesContext:** Se especializa en manejar los contratos realizados sobre diferentes propiedades
- **ClientManager:** Expone la información a los usuarios finales de aquellas propiedades que ya han completado el flujo de investigación y auditoria

### Decisiones de diseño

Con un enfoque de **Microservicios** se ve favorecida la **modularidad** para implementar interfaces o adaptadores que permitan la comunicación con servicios externos de los cuales no hay un estándar establecido de comunicación.

la comunicación asíncrona, como un patrón orientado a **eventos**, es ideal para escenarios donde se necesita **desacoplar** los componentes y manejar **grandes volúmenes de datos**, al manejar una comunicación **asíncrona** se permite gestionar el flujo de la información a partir de eventos que son desencadenados por actualizaciones de la información.

### Puntos de sensibilidad detectados

Se identifican dos cuellos de botella importantes para los servicios de *Property* y *DataAudit* estos microservicios deben manejar un gran volumen de solicitudes y concurrencia

## Escenarios de calidad a probar

### **Escenario 1:** Alta Concurrencia en Eventos de Dominio (Refined by Nicolay)

- *Descripción:* Tiempo de respuesta en el servicio - de *Propiedades* debe
- *Estímulo:* Alto volumen transaccional a nivel de operaciones requeridas por el servicio de Propiedades
- *Ambiente:* Operación bajo estrés
- *Artefacto:* Microservicio de Propiedades, Broker
- *Respuesta:* El microservicio responde adecuadamente a las solicitudes de usuarios concurrentes
- *Medida de la respuesta:* Se calcula que el servicio va a procesar en promedio de acuerdo con los datos del enunciado un aprox de
Propiedades promedio por país: 260K
Operaciones promedio por propiedad (micros publicadores): 2
Es decir que en total pueda procesar 520k transacciones sin generar fallos en el sistema.
- *Decisiones  Arquitecturales:*
  - Puntos de sensibilidad: El microservicio de Propiedades debe ser capaz de soportar la integridad de la información y así mismo el broker debe poder soportar el volumen de datos.
  - Tradeoff: Impacto en la complejidad  del sistema y en el auto-escalado
  - Riesgo: Sobredimensionamiento, Saturación de cola de mensajes
configurado
- *Justificación:* Cuantitativamente,  la gestión de colas de mensajes  optimiza el flujo de solicitudes, desacoplando las operaciones asegurando  tiempos de respuesta más rápidos he independientes.  Cualitativamente,  el desacoplamiento  mediante  eventos  de dominio aumenta la independencia  y la robustez  de los servicios,  mejorando  la gestión de carga y la mantenibilidad del sistema.

### **Escenario 4:** Integración de Nuevos Mercados (Refined by Juan)

- *Descripción:* Agregar soporte para un nuevo mercado con reglas de negocio y terminología local.
- *Estímulo:* Requerimiento para soportar un nuevo país con sus especificidades legales y de negocio.
- *Ambiente:* Desarrrollo
- *Artefacto:* Microservicio de información corporativa
- *Respuesta:* El sistema incorpora el nuevo mercado sin afectar los existentes.
- *Medida de la respuesta:* Incorporación en menos de 2 semanas.
- *Decisiones  Arquitecturales:*
  - *Microservicio DataAdapter*
    - Puntos de sensibilidad: Rendimiento óptimo a la hora de acceder a los datos.
    - Tradeoff: La capacidad de adaptación puede afectar la facilidad de mantenimiento y entendimiento del código.
    - Riesgo: Dada la cantidad de diferentes regiones que se pueden cubrir, puede haber cierto tipo de datos que no puedan ser manejados adecuadamente.
  - *Pull a servicios externos*
    - Puntos de sensibilidad: Sensibilidad en el tiempo de obtener los datos.
    - Tradeoff: Mayor control de los datos pero puede haber retardo en actualización
    - Riesgo: La seguridad de pull de datos debe ser más robusta.
- *Justificación:* La arquitectura basada en microservicios facilita la expansión a nuevos mercados al permitir la adición de servicios específicos por mercado, manteniendo el sistema cohesivo y manejable.

### **Escenario 8:** Actualización de datos (Refined by Luis)  
- *Descripción:* Mantener la consistencia de datos entre microservicios relacionados.
- *Estímulo:* Ejecución de la auditoria de datos para verificación de confiabilidad
- *Ambiente:* Operación normal en desarrollo y producción
- *Artefacto:* Miroservicio de data audit
- *Respuesta:* Obtención de los indices de confiabilidad de los datos 
- *Medida de la respuesta:* Deben generarse en menos de 2 segundos.
- *Decisiones  Arquitecturales:*
    - Puntos de sensibilidad: Actualziación de los datos y complejidad en la gestión de eventos
    - Tradeoff:	El uso de tópicos incremente la latencia entre microservicios y la complejidad de publicación, suscripción y enrutamiento de eventos puede agregar complejidad al sistema
    - Riesgo: No tener los valores de confiabilidad actualizados
- *Justificación:*  La propagación de eventos asegura la coherencia entre los microservisios, escencial para la interoperabilidad efectiva dentro de una arquitectura basada en eventos. 

### TODO:

#### [✅] Refinar y elegir los tres escenarios de calidad que vamos a utilizar con base en los comentarios de la entrega anterior

*Escenarios:*
*Escenario 1:* Tiempo de respuesta en el servicio de *Propiedades*

*Escenario 4:* Agregar soporte para un nuevo mercado con reglas de negocio y terminología local. !! *(Propiedades, DataAdapter)*

*Escenario 8:* Mantener la consistencia de datos entre microservicios relacionados. !! *DataAudit*

Tentativo?:
*Escenario nuevo?* donde se evidencie la necesidad de escalar ciertos microservicio con alta demanda  (Rendimiento - cuello de botella) para el caso se podría utilizar el servicio de *DataAudit*

#### [ ] Diseñar e implementar 3 microservicios para satisfacer 3 de los escenarios de calidad definidos en la entrega pasada

#### [ ] Desarrollo como mínimo 3 microservicios con comunicación basada en eventos y comandos

(Sacar un microservicio genérico que aplique y replicarlos dos veces para el total de tres microservicios)

Cada micro debe estar por capas (cebolla) (Repositorios, lógica, enrutamiento, objetovalor...)

#### [ ] La comunicación de todos los microservicios se hace por medio de comandos y eventos (PULSAR)

Pulsar debe ser configurado ya sea en la infraestructura (AWS o GCP (Como Pub/Sub) o como un componente aparte)

(La única excepción es la ejecución de queries síncronos, donde puede ser usado un protocolo como HTTP o gRPC.)

#### [✅] Deben ser claros los principios de DDD en el diseño: agregaciones, contextos acotados, inversión de dependencias, capas, etc

#### [ ] Usar Apache Pulsar como broker de eventos

(Para la propagación de comandos y eventos, el equipo configuró, desplegó y uso un cluster en Apache Pulsar)

#### [ ] Se justifica correctamente los tipos de eventos a utilizar (integración o carga de estado). Ello incluye la definición de los esquemas y evolución de los mismos (Documentar)

#### [ ] Definir, justificar e implementar alguna de las topologías para la administración de datos descentralizada o híbrida

#### [ ] Definir e implementar un modelo *CRUD* o Event Sourcing en la capa de datos en al menos 3 de los servicios

Nota:
DEBIZIUM: Tiene tabla de transacciones (Manejado por estado) (EventSourcing)

#### [ ] Desplegar en una plataforma de preferencia

#### [✅] El código debe encontrarse en un software de control de versionamiento como Github

[Repositorio](https://github.com/nicolay-dev/monolitics-poc)

#### [ ] Grabar video

#### [ ] Documentar con la descripción de actividades realizada por cada miembro

Refinamiento de los escenarios - todos
Construcción de los micros - La comunicación BD - Nico
configurar en cada micro la comunicación por comandos y eventos
Construir Componente pulsar - luis
Despliegue





Actualizar diagrama para justificar comunicación por eventos

