from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from adapters.db_config import Base, engine
import uuid
# from marshmallow import fields, Schema
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# db = SQLAlchemy()


class PropertyEntity(Base):
    __tablename__ = 'properties'


    id_property = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    external_data = Column(String(100))
    field_research = Column(String(100))
    sales_context = Column(String(100))

    def __repr__(self):
        return f'<PropertyEntity id_property={self.id_property}>'
    
    def to_dict(self):
        return {
            "id_property": self.id_property,
            "external_data": self.external_data,
            "field_research": self.field_research,
            "sales_context": self.sales_context,
        }
        

Base.metadata.create_all(bind=engine)
    