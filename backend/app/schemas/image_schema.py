# Marshmallow schema for Image model
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models.image import Image
from app.utils.s3_helper import S3Helper

class ImageSchema(SQLAlchemyAutoSchema):
    s3_url = fields.Method("get_presigned_url")

    class Meta:
        model = Image
        load_instance = True
        include_fk = True

    def get_presigned_url(self, obj):
        s3_helper = S3Helper()
        # 1 hour expiration
        return s3_helper.s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': s3_helper.bucket, 'Key': obj.s3_key},
            ExpiresIn=3600
        )
