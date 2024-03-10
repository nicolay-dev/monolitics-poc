import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

## Project model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, index=True, nullable=False)
    fullName = db.Column(db.String(500), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    country = db.Column(db.String(512), nullable=True)
    department = db.Column(db.String(512), nullable=True)
    city = db.Column(db.String(512), nullable=True)
    postalCode = db.Column(db.String(512), nullable=True)
    address = db.Column(db.String(512), nullable=True)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    phone = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(512), nullable=True)
    roleID = db.Column(db.Integer, nullable=True)
    bankAccountNumber = db.Column(db.Integer, nullable=True)
    bankAccountId= db.Column(db.Integer, nullable=True)
    createdAt = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    industry = db.Column(db.String(255), nullable=True)
    size =  db.Column(db.String(100), nullable=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    creation_date = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    end_date = db.Column(db.DateTime(timezone=True), nullable=True)


class PersonalProjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False) #id de la empresa
    user_id = db.Column(db.Integer, nullable=False)  #id_del integrante del proyecto
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    fullName = db.Column(db.String(255), nullable=False) #nombre del integrante del proyecto
    technical_profile = db.Column(db.String(255), nullable=True)
    skill_id = db.Column(db.String(255), nullable=True)
    project_role = db.Column(db.String(255), nullable=True)
    technology_id = db.Column(db.String(255), nullable=True)
    hourly_rate = db.Column(db.String(255), nullable=True)

