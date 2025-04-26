# Marshmallow schema for user registration validation
from marshmallow import Schema, fields, validates, ValidationError
import re

class UserRegistrationSchema(Schema):
    username = fields.Str(required=True, validate=lambda s: 3 <= len(s) <= 30)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda p: len(p) >= 8)

    @validates("username")
    def validate_username(self, value, **kwargs):
        if not re.match("^[a-zA-Z0-9_]+$", value):
            raise ValidationError("Username must be alphanumeric with underscores only.")

    @validates("password")
    def validate_password(self, value, **kwargs):
        if not re.search(r"[A-Za-z]", value) or not re.search(r"[0-9]", value):
            raise ValidationError("Password must contain at least one letter and one number.")
