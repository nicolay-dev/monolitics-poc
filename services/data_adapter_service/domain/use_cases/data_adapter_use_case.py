from typing import List
from domain.models.data_adapter_model import DataAdapterModel
from domain.repositories.data_adapter_repository import DataAdapterRepository


class DataAdapterUseCase:
    def __init__(self, data_adapter_repository: DataAdapterRepository):
        self.data_adapter_repository = data_adapter_repository

    def create_data_adapter(self, api_url: str, json_keys: List[str]) -> DataAdapterModel:
        return self.data_adapter_repository.create_data_adapter(api_url, json_keys)

    def get_data_adapter_by_id(self, data_adapter_id: int) -> DataAdapterModel:
        return self.data_adapter_repository.get_data_adapter_by_id(data_adapter_id)

    def get_data_adapters(self) -> DataAdapterModel:
        return self.data_adapter_repository.get_data_adapters()

    def update_data_adapter(self, data_adapter: DataAdapterModel) -> DataAdapterModel:
        return self.data_adapter_repository.update_data_adapter(data_adapter)

    def delete_data_adapter(self, data_adapter_id: int) -> None:
        return self.data_adapter_repository.delete_data_adapter(data_adapter_id)
