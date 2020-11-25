##from datetime import datetime

from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.models import BaseModel
from config import Config


db = SQLAlchemy(model_class=BaseModel)
migrate = Migrate(compare_type=True)
ma = Marshmallow()
docs = FlaskApiSpec()


def create_app(config_class=Config):
    # Configure app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register API blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

##    # Register API documentation
##    ## Acknowledgements
##    from app.api import acknowledgments as api_ackn
##    docs.register(api_ackn.list_acknowledgments, blueprint='api')
##    docs.register(api_ackn.create_acknowledgment, blueprint='api')
##    docs.register(api_ackn.get_acknowledgment, blueprint='api')
##    docs.register(api_ackn.export_acknowledgment, blueprint='api')
##    docs.register(api_ackn.update_acknowledgment, blueprint='api')
##    docs.register(api_ackn.delete_acknowledgment, blueprint='api')
##    
##    ## Involvements
##    from app.api import involvements as api_invo
##    docs.register(api_invo.list_involvements, blueprint='api')
##    docs.register(api_invo.create_involvement, blueprint='api')
##    docs.register(api_invo.get_involvement, blueprint='api')
##    docs.register(api_invo.export_involvement, blueprint='api')
##    docs.register(api_invo.update_involvement, blueprint='api')
##    docs.register(api_invo.delete_involvement, blueprint='api')
##
##    ## Notes
##    from app.api import notes as api_note
##    docs.register(api_note.list_notes, blueprint='api')
##    docs.register(api_note.create_note, blueprint='api')
##    docs.register(api_note.get_note, blueprint='api')
##    docs.register(api_note.export_note, blueprint='api')
##    docs.register(api_note.update_note, blueprint='api')
##    docs.register(api_note.delete_note, blueprint='api')
##    
    ## Vulnerabilities
    from app.api import vulnerability as api_vuln
##    docs.register(api_vuln.list_vulnerabilities, blueprint='api')
    docs.register(api_vuln.create_vulnerability, blueprint='api')
##    docs.register(api_vuln.get_vulnerability, blueprint='api')
##    docs.register(api_vuln.export_vulnerability, blueprint='api')
##    docs.register(api_vuln.update_vulnerability, blueprint='api')
##    docs.register(api_vuln.delete_vulnerability, blueprint='api')
##    docs.register(api_vuln.add_acknowledgments, blueprint='api')
##    docs.register(api_vuln.delete_acknowledgments, blueprint='api')
##    docs.register(api_vuln.add_involvements, blueprint='api')
##    docs.register(api_vuln.delete_involvements, blueprint='api')
##    docs.register(api_vuln.add_notes, blueprint='api')
##    docs.register(api_vuln.delete_notes, blueprint='api')

    # Register Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    docs.init_app(app)

    return app
