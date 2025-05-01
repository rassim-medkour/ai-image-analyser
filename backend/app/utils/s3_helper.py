import boto3
from botocore.exceptions import ClientError
from flask import current_app

class S3Helper:
    """
    Helper class for S3-compatible storage operations (AWS S3, Cloudflare R2, etc.)
    Provides unified interface for file uploads, downloads, URL generation,
    and other storage operations. Built upon boto3 SDK with support for
    alternative endpoints like Cloudflare R2.
    """
    def __init__(self):
        """
        Initialize S3 client using configuration from Flask app.
        Supports custom endpoints for S3-compatible services (like Cloudflare R2).
        Configuration parameters are loaded from environment variables via Flask config.
        """
        # Safely retrieve configuration with fallbacks
        region = current_app.config.get('S3_REGION')
        endpoint = current_app.config.get('S3_ENDPOINT_URL')
        
        # Build boto3 client configuration dictionary with required credentials
        client_kwargs = {
            'aws_access_key_id': current_app.config['S3_ACCESS_KEY'],
            'aws_secret_access_key': current_app.config['S3_SECRET_KEY']
        }
        # Only add optional parameters if they exist to avoid errors
        if region:
            client_kwargs['region_name'] = region
        if endpoint:
            client_kwargs['endpoint_url'] = endpoint
            
        # Initialize the boto3 S3 client with our configuration
        self.s3_client = boto3.client('s3', **client_kwargs)
        self.bucket = current_app.config['S3_BUCKET_NAME']

    def upload_file(self, file_obj, key, content_type):
        """
        Upload a file to S3-compatible storage and generate access URL.
        
        Args:
            file_obj: File-like object containing the data to upload
            key: Destination path/key within the S3 bucket
            content_type: MIME type of the file (e.g., 'image/jpeg')
            
        Returns:
            str: Generated URL for the uploaded file
            
        Raises:
            RuntimeError: If upload fails due to S3 errors
        """
        try:
            # Use Boto3 to upload the file with specified metadata
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket,
                key,
                ExtraArgs={'ContentType': content_type}
            )
            
            # Generate a URL to access the file after upload
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=0  # 0 means no expiration, or set as needed
            )
            return url
        except ClientError as e:
            # Wrap boto3 exceptions with our custom exception for better error handling
            # Use 'from e' to preserve the original exception chain for debugging
            raise RuntimeError(f"S3 upload failed: {e}") from e
            
    def get_presigned_url(self, key, expires=3600):
        """
        Generate a pre-signed URL for an object with a specified expiration time.
        Pre-signed URLs allow temporary direct access to private S3 objects.
        
        Args:
            key (str): The S3 object key (path within bucket)
            expires (int): Expiration time in seconds (default: 1 hour)
            
        Returns:
            str: Pre-signed URL with expiration timeout, or None if generation fails
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=expires
            )
            return url
        except ClientError as e:
            # Log the error but don't raise to avoid disrupting the caller
            current_app.logger.error(f"Failed to generate presigned URL: {str(e)}")
            return None

    def delete_file(self, key):
        """
        Delete a file from S3-compatible storage.
        
        Args:
            key: Path/key of the object to delete within the S3 bucket
            
        Raises:
            RuntimeError: If deletion fails due to S3 errors
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket, Key=key)
        except ClientError as e:
            # Wrap boto3 exceptions with our custom exception for better error handling
            raise RuntimeError(f"S3 delete failed: {e}") from e
