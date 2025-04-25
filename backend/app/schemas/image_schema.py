# Marshmallow schema for Image model
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.image import Image

class ImageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Image
        load_instance = True
        include_fk = True
