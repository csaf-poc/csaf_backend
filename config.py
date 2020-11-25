from dotenv import load_dotenv
from os import environ, path


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or 'change-me'
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME') or 'session'
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI') or \
                              'sqlite:///{}'.format(path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APISPEC_TITLE = 'CSAF Vulnerabilities'
    APISPEC_VERSION = 'v0.1'
    CVSS_V2_SCHEMA = environ.get('CVSS_V2_SCHEMA') or path.join(basedir, 'app/schemas/cvss-v2.0.json')
    CVSS_V3_0_SCHEMA = environ.get('CVSS_V3_0_SCHEMA') or path.join(basedir, 'app/schemas/cvss-v3.0.json')
    CVSS_V3_1_SCHEMA = environ.get('CVSS_V3_1_SCHEMA') or path.join(basedir, 'app/schemas/cvss-v3.1.json')
