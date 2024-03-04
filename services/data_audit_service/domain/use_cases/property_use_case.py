from typing import List
from domain.models.property_model import PropertyModel
from domain.repositories.property_repository import PropertyRepository


class PropertyUseCase:
    def __init__(self, property_repository: PropertyRepository):
        self.property_repository = property_repository

    def create_property(self, property: PropertyModel) -> PropertyModel:
        return self.property_repository.create_property(property)

    def get_property(self, property_id: int) -> PropertyModel:
        return self.property_repository.get_property_by_id(property_id)

    def get_properties(self) -> PropertyModel:
        return self.property_repository.get_properties()

    def update_property(self, property: PropertyModel) -> PropertyModel:
        return self.property_repository.update_property(property)

    def delete_property(self, property_id: int) -> None:
        return self.property_repository.delete_property(property_id)
