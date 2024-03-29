from flask import Blueprint, Flask, jsonify, request
import pulsar
from adapters.data_adapter_repository_adapter import DataAdapterRepositoryAdapter
from domain.use_cases.data_adapter_use_case import DataAdapterUseCase
from domain.models.data_adapter_model import DataAdapterModel

api_rest_blueprint = Blueprint('api_rest', __name__)

client = pulsar.Client('pulsar://localhost:6650')
producer = client.create_producer('persistent://public/default/comando-data-adapter-topic')

data_adapter_repository = DataAdapterRepositoryAdapter()
data_adapter_use_case = DataAdapterUseCase(data_adapter_repository)

class ApiRest:

    @api_rest_blueprint.route('/api/ping', methods=['GET'])
    def test_api():
        response = 'pong'
        return {
            "response": response
        }

    @api_rest_blueprint.route('/api/add-data_adapter', methods=['POST'])
    def add_data_adapter_api():
        data: dict = request.get_json()

        api_url = data.get('api_url')
        json_keys = data.get('json_keys', [])

        response = data_adapter_use_case.create_data_adapter(api_url, json_keys)
        
        message = str(data).encode('utf-8')
        producer.send(message)
        
        
        return {
            "response": response
        }
    
    @api_rest_blueprint.route('/api/get-data_adapter/<int:data_adapter_id>', methods=['GET'])
    def get_data_adapter_api(data_adapter_id : int):
        data_adapter = data_adapter_use_case.get_data_adapter_by_id(data_adapter_id)
        return {
            "data_adapter": data_adapter
        }
    
    @api_rest_blueprint.route('/api/update-data_adapter', methods=['PUT'])
    def update_data_adapter_api():
        data: dict = request.get_json()
        data_adapter_data = DataAdapterModel(
            external_data = data.get('external_data'),
        )
        response = data_adapter_use_case.update_data_adapter(data_adapter_data)
        return {
            "response": response
        }
    
    @api_rest_blueprint.route('/api/get-data_adapters', methods=['GET'])
    def get_data_adapters_api():
        data_adapters = data_adapter_use_case.get_data_adapters()
        return {
            "data_adapters": data_adapters
        }

    @api_rest_blueprint.route('/api/delete-data_adapter/<int:data_adapter_id>', methods=['DELETE'])
    def delete_data_adapter_api(data_adapter_id: int):
        response = data_adapter_use_case.delete_data_adapter(data_adapter_id)
        return { 'message': response }, 200
    
