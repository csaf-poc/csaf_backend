from dotenv import load_dotenv
from os import environ, path


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'change-me'
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME') or 'session'
    MONGODB_DB = environ.get('MONGODB_DB') or 'csaf'
    MONGODB_HOST = environ.get('MONGODB_HOST') or 'localhost'
    MONGODB_PORT = environ.get('MONGODB_PORT') or 27017
    CSAF_V2_SCHEMA = environ.get('CSAF_V2_SCHEMA') or path.join(basedir, 'app/schemas/csaf_json_schema.json')
