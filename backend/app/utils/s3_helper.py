import boto3
from botocore.exceptions import ClientError
from flask import current_app

class S3Helper:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=current_app.config['S3_ACCESS_KEY'],
            aws_secret_access_key=current_app.config['S3_SECRET_KEY'],
            region_name=current_app.config['S3_REGION','auto'],
            endpoint_url=current_app.config.get('S3_ENDPOINT_URL')
        )
        self.bucket = current_app.config['S3_BUCKET_NAME']

    def upload_file(self, file_obj, key, content_type):
        try:
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket,
                key,
                ExtraArgs={'ContentType': content_type}
            )
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=0  # 0 means no expiration, or set as needed
            )
            return url
        except ClientError as e:
            raise RuntimeError(f"S3 upload failed: {e}")

    def delete_file(self, key):
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=key)
        except ClientError as e:
            raise RuntimeError(f"S3 delete failed: {e}")
