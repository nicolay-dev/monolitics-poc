from flask import Blueprint, Flask, jsonify, request
import pulsar
from adapters.property_audit_repository_adapter import PropertyAuditRepositoryAdapter
from domain.use_cases.property_audit_use_case import PropertyUseCase
from domain.models.property_audit_model import PropertyAuditModel

api_rest_blueprint = Blueprint('api_rest', __name__)

client = pulsar.Client('pulsar://localhost:6650')
producer = client.create_producer('persistent://public/default/comando-propiedades-audit-topic')

property_audit_repository = PropertyAuditRepositoryAdapter()
property_use_case = PropertyUseCase(property_audit_repository)

class ApiRest:

    @api_rest_blueprint.route('/api/ping', methods=['GET'])
    def test_api():
        response = 'pong'
        return {
            "response": response
        }

    @api_rest_blueprint.route('/api/add-property-audit', methods=['POST'])
    def add_property_api():
        data: dict = request.get_json()
        property_data = PropertyAuditModel(
            id_property=data.get('id_property'),
            external_data = data.get('external_data'),
            field_research = data.get('field_research'),
            sales_context = data.get('sales_context'),
            score_audit = data.get('score_audit')
        )
        response = property_use_case.create_property(property_data)
        message = str(data).encode('utf-8')
        
        producer.send(message)
        return {
            "response": response
        }, 200
    
    @api_rest_blueprint.route('/api/get-property-audit/<int:id_property>', methods=['GET'])
    def get_property_api(id_property : int):
        property = property_use_case.get_property(id_property)
        return {
            "property": property
        }
    
    @api_rest_blueprint.route('/api/update-property-audit', methods=['PUT'])
    def update_property_api():
        data: dict = request.get_json()
        property_data = PropertyAuditModel(
            id_property= data.get('id_property'),
            external_data = data.get('external_data'),
            field_research = data.get('field_research'),
            sales_context = data.get('sales_context'),
            score_audit = data.get('score_audit')
        )
        response = property_use_case.update_property(property_data)
        return {
            "response": response
        }
    
    @api_rest_blueprint.route('/api/get-properties-audit', methods=['GET'])
    def get_properties_api():
        properties = property_use_case.get_properties()
        return {
            "properties": properties
        }

    @api_rest_blueprint.route('/api/delete-properties/<int:id_property>', methods=['DELETE'])
    def delete_property_api(id_property: int):
        response = property_use_case.delete_property(id_property)
        return { 'message': response }, 200
