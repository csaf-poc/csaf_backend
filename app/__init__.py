from flask import Flask
from flask_mongoengine import MongoEngine

from config import Config


db = MongoEngine()


def create_app(config_class=Config):
    # Configure app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register API blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register Flask extensions
    db.init_app(app)

    return app
