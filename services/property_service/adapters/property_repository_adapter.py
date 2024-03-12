from domain.models.property_model import PropertyModel
from domain.repositories.property_repository import PropertyRepository
from adapters.entities.property_entity import PropertyEntity
from adapters.db_config import db


class PropertyRepositoryAdapter(PropertyRepository):

    def create_property(self, property: PropertyModel) -> PropertyModel:
        try:
            db_es = PropertyEntity(
                # id_property = property.id_property,
                external_data = property.external_data,
                field_research = property.field_research,
                sales_context = property.sales_context
            )
            db.add(db_es)
            db.commit()
            return db_es.to_dict()
        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error creando la propiedad, revisar {exception}'
            )

    def get_property_by_id(self, id_property: str) -> PropertyModel:
        try:
            db_es = (db.query(PropertyEntity).filter(PropertyEntity.id_property == id_property).first())
            if db_es is not None:
                return db_es.to_dict()
            return None
        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error creando obteniendo la propiedad, revisar {exception}'
            )

    def get_properties(self) -> PropertyModel:
        try:
            db_es = db.query(PropertyEntity).all()
            return [
                es.to_dict()
                for es in db_es
            ]
        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error obteniendo las propiedades, revisar {exception}'
            )

    def update_property(self, id_property: str, property: PropertyModel) -> PropertyModel:
        try:

            db_es = (db.query(PropertyEntity).filter(PropertyEntity.id_property == id_property).first())

            db_es.id_property = db_es.id_property
            db_es.external_data = property.external_data
            db_es.field_research = property.field_research
            db_es.sales_context = property.sales_context
            db.commit()

            return db_es.to_dict()

        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error actualizando la propiedad, revisar {exception}'
            )

    def delete_property(self, id_property: str):
        try:

            db_es = (db.query(PropertyEntity).filter(PropertyEntity.id_property == id_property).first())
            db.delete(db_es)
            db.commit()
            return True

        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error eliminando la propiedad, revisar {exception}'
            )
