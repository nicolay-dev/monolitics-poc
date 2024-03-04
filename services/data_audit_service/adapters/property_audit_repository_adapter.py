from domain.models.property_audit_model import PropertyAuditModel
from domain.repositories.property_audit_repository import PropertyAuditRepository
from adapters.entities.property_audit_entity import PropertyAuditEntity
from adapters.db_config import db


class PropertyAuditRepositoryAdapter(PropertyAuditRepository):

    def create_property(self, property: PropertyAuditModel) -> PropertyAuditModel:
        try:
            db_es = PropertyAuditEntity(
                id_property = property.id_property,
                external_data = property.external_data,
                field_research = property.field_research,
                sales_context = property.sales_context,
                score_audit = property.score_audit
            )
            db.add(db_es)
            db.commit()
        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error creando la propiedad, revisar {exception}'
            )

    def get_property_by_id(self, property_id: int) -> PropertyAuditModel:
        try:
            db_es = (db.query(PropertyAuditEntity).filter(PropertyAuditEntity.id_property == property_id).first())
            if db_es is not None:
                return PropertyAuditModel(
                    id_property=db_es.id_property,
                    external_data=db_es.external_data,
                    field_research=db_es.field_research,
                    sales_context=db_es.sales_context,
                    score_audit=db_es.score_audit
                ).to_dict()
            return None
        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error creando obteniendo la propiedad, revisar {exception}'
            )

    def get_properties(self) -> PropertyAuditModel:
        try:
            db_es = db.query(PropertyAuditEntity).all()
            return [
                PropertyAuditModel(
                    id_property = es.id,
                    external_data = es.external_data,
                    field_research = es.field_research,
                    sales_context = es.sales_context,
                    score_audit = es.score_audit
                ).to_dict()
                for es in db_es
            ]            
            db.add(db_es)
            db.commit()
        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error obteniendo las propiedades, revisar {exception}'
            )

    def update_property(self, property: PropertyAuditModel) -> PropertyAuditModel:
        try:

            db_es = (db.query(PropertyAuditEntity).filter(PropertyAuditEntity.id_property == property.property_id).first())

            db_es.external_data = property.external_data
            db_es.field_research = property.field_research
            db_es.sales_context = property.sales_context
            db_es.score_audit = property.score_audit
            db.commit()

        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error actualizando la propiedad, revisar {exception}'
            )

    def delete_property(self, property_id: int) -> None:
        try:

            db_es = (db.query(PropertyAuditEntity).filter(PropertyAuditEntity.id_property == property_id).first())
            db.delete(db_es)
            db.commit()

        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error eliminando la propiedad, revisar {exception}'
            )
