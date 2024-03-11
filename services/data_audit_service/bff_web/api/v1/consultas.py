
import strawberry
from .esquemas import *

@strawberry.type
class Query:
    propiedadesAudit: typing.List[PropiedadAudit] = strawberry.field(resolver=obtener_propiedades_audit)