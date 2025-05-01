import boto3
from botocore.exceptions import ClientError
from flask import current_app

class S3Helper:
    def __init__(self):
        # Safely get configuration values with string defaults
        region = current_app.config.get('S3_REGION')
        endpoint = current_app.config.get('S3_ENDPOINT_URL')
        
        # Build boto3 client configuration
        client_kwargs = {
            'aws_access_key_id': current_app.config['S3_ACCESS_KEY'],
            'aws_secret_access_key': current_app.config['S3_SECRET_KEY']
        }
        # Only add optional parameters if they exist
        if region:
            client_kwargs['region_name'] = region
        if endpoint:
            client_kwargs['endpoint_url'] = endpoint
        self.s3_client = boto3.client('s3', **client_kwargs)
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
            
    def get_presigned_url(self, key, expires=3600):
        """
        Generate a pre-signed URL for an object with a specified expiration time.
        
        Args:
            key (str): The S3 object key
            expires (int): Expiration time in seconds (default: 1 hour)
            
        Returns:
            str: Pre-signed URL with expiration
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=expires
            )
            return url
        except ClientError as e:
            current_app.logger.error(f"Failed to generate presigned URL: {str(e)}")
            return None

    def delete_file(self, key):
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=key)
        except ClientError as e:
            raise RuntimeError(f"S3 delete failed: {e}")
