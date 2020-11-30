from dotenv import load_dotenv
from os import environ, path


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'CHANGE-ME'
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME') or 'session'

    # mongoengine
    MONGODB_DB = environ.get('MONGODB_DB') or 'csaf_advisory_db'
    MONGODB_USERNAME = environ.get('MONGODB_USERNAME') or 'csaf_advisory_user'
    MONGODB_PASSWORD = environ.get('MONGODB_PASSWORD') or 'CHANGE-ME'
    MONGODB_HOST = environ.get('MONGODB_HOST') or 'localhost'
    MONGODB_PORT = environ.get('MONGODB_PORT') or 27017
    
    CSAF_V2_SCHEMA = environ.get('CSAF_V2_SCHEMA') or path.join(basedir, 'app/schemas/csaf_json_schema.json')
    SWAGGER_CONFIG = {
        'headers': [],
        'specs': [
            {
                'endpoint': 'api',
                'route': '/csaf_api.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        'static_url_path': '/flasgger_static',
        'swagger-ui': True,
        'specs_route': '/api/specs/'
    }
    SWAGGER_TEMPLATE = {
        'swagger': '2.0',
        'info': {
            'title': 'CSAF API',
            'description': 'API to manage advisories according to the Common Security Advisory Framework v2 standard.',
            'contact': {
                'responsibleOrganization': 'Cyber-Defense Campus armasuisse W+T',
                'responsibleDeveloper': 'Damian Pfammatter',
                'email': 'damian.pfammatter@armasuisse.ch',
            },
            'version': '0.1'
        },
        'schemes': ['http', 'https']
    }
