from dotenv import load_dotenv
import json
from os import environ, path


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    # flask
    SECRET_KEY = environ.get('SECRET_KEY') or 'CHANGE-ME'
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME') or 'session'
    # mongoengine
    MONGODB_DB = environ.get('MONGODB_DB', 'csaf_advisory_db') 
    MONGODB_USERNAME = environ.get('MONGODB_USERNAME', None)
    MONGODB_PASSWORD = environ.get('MONGODB_PASSWORD', None)
    MONGODB_HOST = environ.get('MONGODB_HOST', 'localhost')
    MONGODB_PORT = int(environ.get('MONGODB_PORT', 27017))
    # swagger
    CSAF_V2_SCHEMA = environ.get('CSAF_V2_SCHEMA') or path.join(basedir, 'app/schemas/csaf_json_schema.json')
    SWAGGER_CONFIG = {
        'headers': [],
        'specs': [
            {
                'endpoint': 'api',
                'route': '/api/csaf_api.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        'static_url_path': '/api/flasgger_static',
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
    # oidc
    OIDC_RESOURCE_SERVER_ONLY = True
    OIDC_CLIENT_SECRETS = 'oidc_client_secrets.json'
    with open(OIDC_CLIENT_SECRETS, 'w') as oidc_client_secrets:
        json.dump({
            'web': {
                'issuer': environ.get('OIDC_ISSUER'),
                'auth_uri': environ.get('OIDC_AUTH_URI'),
                'client_id': environ.get('OIDC_CLIENT_ID'),
                'client_secret': environ.get('OIDC_CLIENT_SECRET'),
                'redirect_uris': environ.get('OIDC_REDIRECT_URIS', '*').split(','),
                'userinfo_uri': environ.get('OIDC_USERINFO_URI'),
                'token_uri': environ.get('OIDC_TOKEN_URI'),
                'token_introspection_uri': environ.get('OIDC_INTROSPECTION_URI')
            }
        }, oidc_client_secrets)
    
