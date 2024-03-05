from abc import ABC, abstractmethod
from typing import List
from domain.models.data_adapter_model import DataAdapterModel

# Clases abstractas, interfaces que se van a implementar

class DataAdapterRepository(ABC):
    @abstractmethod
    def create_data_adapter(self, data_adapter: DataAdapterModel) -> DataAdapterModel:
        pass

    @abstractmethod
    def get_data_adapter_by_id(self, data_adapter_id: int) -> DataAdapterModel:
        pass

    @abstractmethod
    def get_data_adapters(self) -> DataAdapterModel:
        pass
    
    @abstractmethod
    def update_data_adapter(self, data_adapter: DataAdapterModel) -> DataAdapterModel:
        pass

    @abstractmethod
    def delete_data_adapter(self, data_adapter_id: int) -> None:
        pass