from flask import Flask, jsonify, request
import pulsar
from adapters.property_audit_repository_adapter import PropertyAuditRepositoryAdapter
from domain.use_cases.property_audit_use_case import PropertyUseCase
from domain.models.property_audit_model import PropertyAuditModel


app = Flask(__name__)

client = pulsar.Client('pulsar://localhost:6650')

producer = client.create_producer('persistent://public/default/comando-propiedades-audit-topic')

property_audit_repository = PropertyAuditRepositoryAdapter()
property_use_case = PropertyUseCase(property_audit_repository)

class ApiRest:

    @app.route('/api/ping', methods=['GET'])
    def test_api():
        response = 'pong'
        return {
            "response": response
        }

    @app.route('/api/add-property-audit', methods=['POST'])
    def add_property_api():
        data: dict = request.get_json()
        property_data = PropertyAuditModel(
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
        }
    
    @app.route('/api/get-property-audit/<int:property_id>', methods=['GET'])
    def get_property_api(property_id : int):
        property = property_use_case.get_property(property_id)
        return {
            "property": property
        }
    
    @app.route('/api/update-property-audit', methods=['PUT'])
    def update_property_api():
        data: dict = request.get_json()
        property_data = PropertyAuditModel(
            external_data = data.get('external_data'),
            field_research = data.get('field_research'),
            sales_context = data.get('sales_context'),
            score_audit = data.get('score_audit')
        )
        response = property_use_case.update_property(property_data)
        return {
            "response": response
        }
    
    @app.route('/api/get-properties-audit', methods=['GET'])
    def get_properties_api():
        properties = property_use_case.get_properties()
        return {
            "properties": properties
        }

    @app.route('/api/delete-properties/<int:property_id>', methods=['DELETE'])
    def delete_property_api(property_id: int):
        return property_use_case.delete_property(property_id)
