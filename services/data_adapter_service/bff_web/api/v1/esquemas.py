import typing
import strawberry
import requests
import os

from datetime import datetime


HOST = os.getenv("URL_DATA_ADAPTERS", default="localhost")

def obtener_datos(root) -> typing.List["Datos"]:
    datos_json = requests.get(f'http://{HOST}:5000/api/get-data_adapters').json()
    datos = []

    for dato in datos_json.get('data_adapters', []):
            external_data_dict = {}
            try:
                external_data_dict = dict(item.split(': ') for item in dato.get('external_data', '').split(', '))
            except ValueError as e:
                print(f"Error parsing external_data: {e}")

            id_adapter = external_data_dict.get('id')

            datos.append(
                Datos(
                    id=id_adapter,
                    datos_extraidos=dato.get('external_data', '')
                )
            )

    return datos

@strawberry.type
class Datos:
    id: str
    datos_extraidos: str

@strawberry.type
class DatosRespuesta:
    mensaje: str
    codigo: int






