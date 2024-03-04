from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from adapters.db_config import Base, engine

# from marshmallow import fields, Schema
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# db = SQLAlchemy()


class PropertyEntity(Base):
    __tablename__ = 'properties'

    id_property = Column(Integer, primary_key=True, index=True)
    external_data = Column(String(100))
    field_research = Column(String(100))
    sales_context = Column(String(100))


class PropertyAuditEntity(Base):
    __tablename__ = 'properties_audit' 

    id_property = Column(Integer, primary_key=True, index=True)
    external_data = Column(String(100))
    field_research = Column(String(100))
    sales_context = Column(String(100))     
    score_audit = Column(String(100))

Base.metadata.create_all(bind=engine)
    