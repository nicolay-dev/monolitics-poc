import typing
import strawberry
import uuid
import requests
import os

from datetime import datetime


PROPIEDADES_HOST = os.getenv("PROPIEDADES_ADDRESS", default="localhost")

def obtener_propiedades_audit(root) -> typing.List["PropiedadAudit"]:
    propiedades_json = requests.get(f'http://{PROPIEDADES_HOST}:5000/api/get-properties-audit').json()
    propiedades = []

    for i in propiedades_json.get('properties', []):
        propiedades.append(
            PropiedadAudit(
                idProperty=i.get('id_property'), 
                externalData=i.get('external_data'), 
                fieldResearch=i.get('field_research'),
                salesContext=i.get('sales_context'),
                scoreAudit=i.get('score_audit')
            )
        )

    return propiedades

@strawberry.type
class PropiedadAudit:
    idProperty: int
    externalData: str
    fieldResearch: str
    salesContext: str
    scoreAudit: str

@strawberry.type
class PropiedadRespuesta:
    mensaje: str
    codigo: int






