from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from adapters.db_config import Base, engine

# from marshmallow import fields, Schema
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# db = SQLAlchemy()


class DataAdapterEntity(Base):
    __tablename__ = 'adapter_entities'

    id_adapter = Column(Integer, primary_key=True, index=True)
    external_data = Column(String(100))

Base.metadata.create_all(bind=engine)
    