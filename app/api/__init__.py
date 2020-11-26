from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException


bp = Blueprint('api', __name__)


@bp.app_errorhandler(Exception)
def handle_exception(e):
    response = jsonify({
        'code': 500,
        'name': 'Internal Server Error',
        'description': ''
    })
    response.status_code = 500
    return response


@bp.app_errorhandler(HTTPException)
def handle_http_exception(e):
    try:
        description = e.data.get('messages').get('json')
    except:
        description = e.description
    
    response = jsonify({
        'code': e.code,
        'name': e.name,
        'description': description
    })
    response.status_code = e.code
    return response


from app.api import advisory
