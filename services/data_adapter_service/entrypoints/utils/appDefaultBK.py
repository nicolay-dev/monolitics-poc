from property_service import create_app
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, JWTManager
from flask_cors import CORS
# from .modelo import db, Usuario

# from services.property_service.app import api_rest

app = create_app('data_adapter_service')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///authenticator.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_SECRET_KEY'] = 'frase-secreta'
# app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
# db.init_app(app)
# db.create_all()

cors = CORS(app)

api = Api(app)

class Pong(Resource):

    def get(self):
        return "Hola Mundo", 200
        
api.add_resource(Pong , '/ping')

jwt = JWTManager(app)