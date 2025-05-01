from datetime import datetime
from app import db

class Image(db.Model):
    """
    Database model representing an uploaded image.
    Defines the structure and relationships for image records in the database.
    
    Key features:
    - Stores both original and storage metadata
    - Maintains user ownership for access control
    - Includes AI-generated description from image analysis
    - Tracks file metadata like size and content type
    """
    __tablename__ = 'images'
    
    # Primary key and identifying fields
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)  # Storage filename (includes path)
    original_filename = db.Column(db.String(255), nullable=False)  # User's original filename
    
    # Storage-related fields
    s3_key = db.Column(db.String(512), nullable=False)  # Key for S3/R2 storage retrieval
    
    # Metadata fields
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)  # When the image was uploaded
    file_size = db.Column(db.Integer)  # Size in bytes
    file_type = db.Column(db.String(50))  # MIME type
    ai_description = db.Column(db.Text, nullable=True)  # AI-generated content description
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Owner reference

    def __repr__(self):
        """String representation of the Image model for debugging and logging"""
        return f'<Image {self.original_filename}>'
