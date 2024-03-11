import strawberry
import typing

from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Despachador

from .esquemas import *

@strawberry.type
class Mutation:

    # TODO Agregue objeto de itinerarios o reserva
    @strawberry.mutation
    async def crear_propiedad(self, id_property1: int, external_data1: str, field_research1: str, sales_context1: str, score_audit1: str, info: Info) -> PropiedadRespuesta:
        print(f"ID propiedad: {id_property1}, Datos externos: {external_data1}, Datos de campo: {field_research1}, Sales context : {sales_context1}, Audit score : {score_audit1}")
        payload = dict(
            id_property = id_property1,
            external_data = external_data1,
            field_research = field_research1,
            sales_context = sales_context1,
            score_audit = score_audit1,
            fecha_creacion = utils.time_millis()
        )
        comando = dict(
            id = str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion = "v1",
            type = "ComandoPropiedad",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name = "BFF Web",
            data = payload
        )
        despachador = Despachador()
        info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "comando-crear-reserva", "public/default/comando-crear-reserva")
        
        return PropiedadRespuesta(mensaje="Procesando Mensaje", codigo=203)