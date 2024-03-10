import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

## Project model
class Transaction(db.Model):
    uuid = db.Column(db.String(50), primary_key=True)
    fact = db.Column(db.String(100), nullable=False)
    resource_tp = db.Column(db.String(100), nullable=False)
    destination_tp = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    


