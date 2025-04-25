# Import models here for easy access if needed
default_models = []
try:
    from .user import User
    from .image import Image
    default_models = [User, Image]
except ImportError:
    pass
