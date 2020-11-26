from flask import abort, jsonify, request, url_for
from jsonschema.exceptions import ValidationError

from app.api import bp
from app.models.advisory import Advisory
from app.schemas.csaf import CsafSchema
from config import Config


csaf_schema = CsafSchema(Config.CSAF_V2_SCHEMA)


@bp.route('/advisory', methods=['POST'])
def create_advisory():
    # Schema validation
    data = request.get_json() or {}
    try:
        csaf_schema.validate(data)
    except ValidationError as e:
        abort(400, e.message)
    # Create and save new advisory
    advisory = Advisory(**data)
    advisory.save()
    # Return response
    response = jsonify(advisory.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_advisory', uid=advisory._id)
    return response


@bp.route('/advisory/<int:uid>', methods=['GET'])
def get_advisory(uid, include_metadata=True):
    advisory = Advisory.objects(_id=uid).first()
    if advisory is None: abort(404, 'Advisory not found.')
    response = jsonify(advisory.to_dict(include_metadata=include_metadata))
    response.status_code = 200
    return response


@bp.route('/advisory/<int:uid>/export', methods=['GET'])
def export_advisory(uid):
    return get_advisory(uid, include_metadata=False)
