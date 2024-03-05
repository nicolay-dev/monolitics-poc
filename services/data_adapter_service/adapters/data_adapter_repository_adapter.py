from domain.models.data_adapter_model import DataAdapterModel
from domain.repositories.data_adapter_repository import DataAdapterRepository
from adapters.entities.data_adapter_entity import DataAdapterEntity
from adapters.db_config import db
import random
import requests


class DataAdapterRepositoryAdapter(DataAdapterRepository):

    def create_data_adapter(self, api_url: str, json_keys: list) -> DataAdapterModel:
        try:

            response = requests.get(api_url)

            if response.status_code == 200:
                api_data = response.json()

                converted_data = ""
                for key in json_keys:
                    if key in api_data:
                        converted_data += f"{key}: {api_data[key]}, "

                id_to_use = db.query(DataAdapterEntity).all()

                if id_to_use:
                    last_id = id_to_use[-1].id_adapter
                else:
                    last_id = 1

                db_es = DataAdapterEntity(
                    id_adapter = last_id + 1,
                    external_data = converted_data[:-2],
                )
                db.add(db_es)
                db.commit()
        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error creando los datos adaptados, revisar {exception}'
            )

    def get_data_adapter_by_id(self, dataAdapter_id: int) -> DataAdapterModel:
        try:
            db_es = (db.query(DataAdapterEntity).filter(DataAdapterEntity.id_adapter == dataAdapter_id).first())
            if db_es is not None:
                return DataAdapterModel(
                    id_adapter=db_es.id_adapter,
                    external_data=db_es.external_data
                ).to_dict()
            return None
        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error obteniendo los datos adaptados, revisar {exception}'
            )

    def get_data_adapters(self) -> DataAdapterModel:
        try:
            db_es = db.query(DataAdapterEntity).all()
            return [
                DataAdapterModel(
                    id_adapter = es.id_adapter,
                    external_data = es.external_data
                ).to_dict()
                for es in db_es
            ]      
        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error obteniendo los datos adaptados, revisar {exception}'
            )

    def update_data_adapter(self, dataAdapter: DataAdapterModel) -> DataAdapterModel:
        try:

            db_es = (db.query(DataAdapterEntity).filter(DataAdapterEntity.id_adapter == dataAdapter.id_adapter).first())

            db_es.external_data = dataAdapter.external_data
            db.commit()

        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error actualizando los datos adaptados, revisar {exception}'
            )

    def delete_data_adapter(self, adapter_id: int) -> None:
        try:

            db_es = (db.query(DataAdapterEntity).filter(DataAdapterEntity.id_adapter == adapter_id).first())
            db.delete(db_es)
            db.commit()

        except Exception as exception:
            raise NameError(
                f'Ha ocurrido un error eliminando los datos adaptados, revisar {exception}'
            )
