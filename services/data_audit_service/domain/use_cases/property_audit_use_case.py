from typing import List
from domain.models.property_audit_model import PropertyAuditModel
from domain.repositories.property_audit_repository import PropertyAuditRepository


class PropertyUseCase:
    def __init__(self, property_repository: PropertyAuditRepository):
        self.property_repository = property_repository

    def create_property(self, property: PropertyAuditModel) -> PropertyAuditModel:
        return self.property_repository.create_property(property)

    def get_property(self, id_property: int) -> PropertyAuditModel:
        return self.property_repository.get_property_by_id(id_property)

    def get_properties(self) -> PropertyAuditModel:
        return self.property_repository.get_properties()

    def update_property(self, property: PropertyAuditModel) -> PropertyAuditModel:
        return self.property_repository.update_property(property)

    def delete_property(self, id_property: int) -> bool:
        return self.property_repository.delete_property(id_property)
