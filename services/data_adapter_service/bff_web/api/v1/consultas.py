
import strawberry
from .esquemas import *

@strawberry.type
class Query:
    datos: typing.List[Datos] = strawberry.field(resolver=obtener_datos)