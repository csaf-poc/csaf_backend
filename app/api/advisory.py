from flask import abort, jsonify, request, url_for

from app.api import bp
from app.api import validate_schema
from app.models.advisory import Advisory
from app.schemas.csaf import CSAFv2Schema


@bp.route('/advisory', methods=['POST'])
@validate_schema(CSAFv2Schema)
def create_advisory():
    # Create and save new advisory
    data = request.get_json() or {}
    advisory = Advisory(**data)
    advisory.save()
    # Return response
    response = jsonify(advisory.to_json())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_advisory', uid=advisory._id)
    return response


@bp.route('/advisory/<int:uid>', methods=['GET'])
def get_advisory(uid, include_metadata=True):
    advisory = Advisory.objects(_id=uid).first()
    if advisory is None: abort(404, 'Advisory not found.')
    response = jsonify(advisory.to_json(include_metadata=include_metadata))
    response.status_code = 200
    return response


@bp.route('/advisory/<int:uid>/export', methods=['GET'])
def export_advisory(uid):
    return get_advisory(uid, include_metadata=False)


##@bp.route('/advisory/<int:uid>', methods=['PUT'])
##@validate_schema(CSAFv2Schema)
##def update_advisory(uid):
##    pass
