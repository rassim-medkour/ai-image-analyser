# App factory: creates and configures the Flask app, registers extensions and blueprints
from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS

# Extensions (initialized later)
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # CORS setup: handles all CORS headers, preflight, credentials, and common issues
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},  # In production, set to your frontend URL
        supports_credentials=True,
        allow_headers=[
            "Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin"
        ],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        expose_headers=["Content-Disposition"]  # For file downloads if needed
    )

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.image import image_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(user_bp, url_prefix="/api/v1/users")
    app.register_blueprint(image_bp, url_prefix="/api/v1/images")

    return app
