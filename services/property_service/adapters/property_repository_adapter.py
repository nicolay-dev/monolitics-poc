from domain.models.property_model import PropertyModel
from domain.repositories.property_repository import PropertyRepository
from adapters.entities.property_entity import PropertyEntity
from adapters.db_config import db


class PropertyRepositoryAdapter(PropertyRepository):

    def create_property(self, property: PropertyModel) -> PropertyModel:
        try:
            db_es = PropertyEntity(
                id_property = property.id_property,
                external_data = property.external_data,
                field_research = property.field_research,
                sales_context = property.sales_context
            )
            db.add(db_es)
            db.commit()
        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error creando la propiedad, revisar {exception}'
            )

    def get_property_by_id(self, property_id: int) -> PropertyModel:
        try:
            db_es = (db.query(PropertyEntity).filter(PropertyEntity.id_property == property_id).first())
            if db_es is not None:
                return PropertyModel(
                    id_property=db_es.id_property,
                    external_data=db_es.external_data,
                    field_research=db_es.field_research,
                    sales_context=db_es.sales_context,
                ).to_dict()
            return None
        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error creando obteniendo la propiedad, revisar {exception}'
            )

    def get_properties(self) -> PropertyModel:
        try:
            db_es = db.query(PropertyEntity).all()
            return [
                PropertyModel(
                    id_property = es.id,
                    external_data = es.external_data,
                    field_research = es.field_research,
                    sales_context = es.sales_context
                ).to_dict()
                for es in db_es
            ]
            
            
            db.add(db_es)
            db.commit()
        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error obteniendo las propiedades, revisar {exception}'
            )

    def update_property(self, property: PropertyModel) -> PropertyModel:
        try:

            db_es = (db.query(PropertyEntity).filter(PropertyEntity.id_property == property.property_id).first())

            db_es.external_data = property.external_data
            db_es.field_research = property.field_research
            db_es.sales_context = property.sales_context
            db.commit()

        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error actualizando la propiedad, revisar {exception}'
            )

    def delete_property(self, property_id: int) -> None:
        try:

            db_es = (db.query(PropertyEntity).filter(PropertyEntity.id_property == property_id).first())
            db.delete(db_es)
            db.commit()

        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error eliminando la propiedad, revisar {exception}'
            )
