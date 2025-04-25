# Marshmallow schema for user login validation
from marshmallow import Schema, fields, validates, ValidationError, validate
import re

class UserLoginSchema(Schema):
    username_or_email = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates("username_or_email")
    def validate_username_or_email(self, value):
        if "@" in value:
            # Validate as email
            email_validator = validate.Email(error="Invalid email format.")
            email_validator(value)
        else:
            # Validate as username (same rules as registration)
            if not (3 <= len(value) <= 30):
                raise ValidationError("Username must be between 3 and 30 characters.")
            if not re.match("^[a-zA-Z0-9_]+$", value):
                raise ValidationError("Username must be alphanumeric with underscores only.")
