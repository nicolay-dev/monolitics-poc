from abc import ABC, abstractmethod
from typing import List
from domain.models.property_model import PropertyModel

# Clases abstractas, interfaces que se van a implementar

class PropertyRepository(ABC):
    @abstractmethod
    def create_property(self, property: PropertyModel) -> PropertyModel:
        pass

    @abstractmethod
    def get_property_by_id(self, id_property: int) -> PropertyModel:
        pass

    @abstractmethod
    def get_properties(self) -> PropertyModel:
        pass
    
    @abstractmethod
    def update_property(self, property: PropertyModel) -> PropertyModel:
        pass

    @abstractmethod
    def delete_property(self, id_property: int) -> bool:
        pass