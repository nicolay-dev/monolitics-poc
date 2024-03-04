from abc import ABC, abstractmethod
from typing import List
from domain.models.property_audit_model import PropertyAuditModel

# Clases abstractas, interfaces que se van a implementar

class PropertyAuditRepository(ABC):
    @abstractmethod
    def create_property(self, property: PropertyAuditModel) -> PropertyAuditModel:
        pass

    @abstractmethod
    def get_property_by_id(self, property_id: int) -> PropertyAuditModel:
        pass

    @abstractmethod
    def get_properties(self) -> PropertyAuditModel:
        pass
    
    @abstractmethod
    def update_property(self, property: PropertyAuditModel) -> PropertyAuditModel:
        pass

    @abstractmethod
    def delete_property(self, property_id: int) -> None:
        pass