from flask import request, abort, Blueprint, jsonify
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


from app.api import vulnerability


##class BaseApi:
##
##    def __init__(self, Model, ModelListSchema):
##        self.Model = Model()
##        self.ModelListSchema = ModelListSchema
##
##    def list(self, endpoint):
##        page = request.args.get('page', 1, type=int)
##        per_page = min(request.args.get('per_page', 10, type=int), 100)
##        models = self.Model.list(page, per_page)
##        models_list = self.ModelListSchema.to_dict(models, page, per_page, endpoint)
##        return models_list, 200
##
##    def create(self, **kwargs):
##        model = self.Model.create(**kwargs)
##        return model, 201
##
##    def get(self, model_id):
##        model = self.Model.get(model_id)
##        if model is None: abort(404, 'Not found.')
##        return model, 200
##
##    def update(self, model_id, **kwargs):
##        model = self.Model.update(model_id, **kwargs)
##        if model is None: abort(404, 'Not found.')
##        return model, 200
##
##    def delete(self, model_id):
##        model = self.Model.delete(model_id)
##        if model is None: abort(404, 'Not found.')
##        return None, 204
##
##
##from app.api import vulnerabilities, notes, involvements, acknowledgments
