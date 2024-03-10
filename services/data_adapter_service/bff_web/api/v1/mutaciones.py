import strawberry
import uuid
from typing import List
from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Despachador

from .esquemas import *

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def crear_data_adapters(self, api_url: str, json_keys: List[str], info: Info) -> DatosRespuesta:
        print(f"URL API: {api_url}, variables JSON: {json_keys}")
        payload = dict(
            url_api = api_url,
            json_list = json_keys,
            fecha_creacion = utils.time_millis()
        )
        comando = dict(
            id = str(uuid.uuid4()),
            time=utils.time_millis(),
            specversion = "v1",
            type = "ComandoDatos",
            ingestion=utils.time_millis(),
            datacontenttype="AVRO",
            service_name = "BFF Web Data Adapter",
            data = payload
        )
        despachador = Despachador()
        info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "comando-data-adapter-topic", "public/default/comando-data-adapter-topic")
        
        return DatosRespuesta(mensaje="Procesando Mensaje", codigo=203)