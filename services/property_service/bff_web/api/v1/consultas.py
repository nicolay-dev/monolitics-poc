
import strawberry
from .esquemas import *

@strawberry.type
class Query:
    propiedades: typing.List[Propiedad] = strawberry.field(resolver=obtener_propiedades)