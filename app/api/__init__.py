from flask import abort, Blueprint, jsonify, request
from functools import wraps
from jsonschema.exceptions import ValidationError
from werkzeug.exceptions import HTTPException


bp = Blueprint('api', __name__)


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


@bp.app_errorhandler(Exception)
def handle_exception(e):
    response = jsonify({
        'code': 500,
        'name': 'Internal Server Error',
        'description': ''
    })
    response.status_code = 500
    return response


def validate_schema(schema):
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            data = request.get_json() or {}
            try:
                schema.validate(data)
            except ValidationError as e:
                abort(400, e.message)
            return view(*args, **kwargs)
        return wrapped_view
    return decorator


from app.api import advisory
