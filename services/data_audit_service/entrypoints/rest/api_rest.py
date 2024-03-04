from flask import Flask, jsonify, request

from adapters.property_repository_adapter import PropertyRepositoryAdapter
from domain.use_cases.property_use_case import PropertyUseCase
from domain.models.property_model import PropertyModel


app = Flask(__name__)


property_repository = PropertyRepositoryAdapter()
property_use_case = PropertyUseCase(property_repository)

class ApiRest:

    @app.route('/api/ping', methods=['GET'])
    def test_api():
        response = 'pong'
        return {
            "response": response
        }

    @app.route('/api/add-property', methods=['POST'])
    def add_property_api():
        data: dict = request.get_json()
        property_data = PropertyModel(
            external_data = data.get('external_data'),
            field_research = data.get('field_research'),
            sales_context = data.get('sales_context'),
        )
        response = property_use_case.create_property(property_data)
        return {
            "response": response
        }
    
    @app.route('/api/get-property/<int:property_id>', methods=['GET'])
    def get_property_api(property_id : int):
        property = property_use_case.get_property(property_id)
        return {
            "property": property
        }
    
    @app.route('/api/update-property', methods=['PUT'])
    def update_property_api():
        data: dict = request.get_json()
        property_data = PropertyModel(
            external_data = data.get('external_data'),
            field_research = data.get('field_research'),
            sales_context = data.get('sales_context'),
        )
        response = property_use_case.update_property(property_data)
        return {
            "response": response
        }
    
    @app.route('/api/get-properties', methods=['GET'])
    def get_properties_api():
        properties = property_use_case.get_properties()
        return {
            "properties": properties
        }

    @app.route('/api/delete-properties/<int:property_id>', methods=['DELETE'])
    def delete_property_api(property_id: int):
        return property_use_case.delete_property(property_id)
