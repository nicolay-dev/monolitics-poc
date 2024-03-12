from flask import Blueprint, Flask, jsonify, request
import pulsar
from adapters.property_repository_adapter import PropertyRepositoryAdapter
from domain.use_cases.property_use_case import PropertyUseCase
from domain.models.property_model import PropertyModel
import uuid

api_rest_blueprint = Blueprint('api_rest', __name__)

client = pulsar.Client('pulsar://localhost:6650')
c_property_tp = client.create_producer('persistent://public/default/comando-property-topic')
e_property_tp = client.create_producer('persistent://public/default/evento-property-topic')

property_repository = PropertyRepositoryAdapter()
property_use_case = PropertyUseCase(property_repository)

class ApiRest:

    @api_rest_blueprint.route('/api/ping', methods=['GET'])
    def test_api():
        response = 'pong'
        return {
            "response": response
        }

    @api_rest_blueprint.route('/api/add-property', methods=['POST'])
    def add_property_api():            
        try:
            data: dict = request.get_json()
            property_data = PropertyModel(
                external_data=data.get('external_data'),
                field_research=data.get('field_research'),
                sales_context=data.get('sales_context'),
            )
            response = property_use_case.create_property(property_data)        
            
            # Generar un ID único de transacción después de crear la propiedad
            transaction_id = str(uuid.uuid4())
            # Agregar el método HTTP a los datos
            data['method'] = 'POST'
            # Agregar el ID único de transacción a los datos
            data['transaction_id'] = transaction_id
            
            message = str(data).encode('utf-8')
            c_property_tp.send(message)
            e_property_tp.send(message)
            
            return {
                "response": response,
                "transaction_id": transaction_id
            }, 200
        except Exception as e:
            return {
                "error": str(e)
            }, 400
    
    @api_rest_blueprint.route('/api/get-property/<id_property>', methods=['GET'])
    def get_property_api(id_property : str):
        property = property_use_case.get_property(id_property)
        return {
            "property": property
        }
    
    @api_rest_blueprint.route('/api/update-property/<id_property>', methods=['PUT'])
    def update_property_api(id_property : str):
        data: dict = request.get_json()
        property_data = PropertyModel(
            external_data = data.get('external_data'),
            field_research = data.get('field_research'),
            sales_context = data.get('sales_context'),
        )
        response = property_use_case.update_property(id_property, property_data)
        return {
            "response": response
        }
    
    @api_rest_blueprint.route('/api/get-properties', methods=['GET'])
    def get_properties_api():
        properties = property_use_case.get_properties()
        return {
            "properties": properties
        }

    @api_rest_blueprint.route('/api/delete-properties/<id_property>', methods=['DELETE'])
    def delete_property_api(id_property: str):
        response = property_use_case.delete_property(id_property)
        return { 'message': response }, 200
