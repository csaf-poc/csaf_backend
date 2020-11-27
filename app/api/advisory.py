from flask import abort, jsonify, request, url_for

from app.api import bp
from app.api import validate_schema
from app.models.advisory import Advisory
from app.schemas.csaf import CSAFv2Schema

# TODO: list_advisory

@bp.route('/advisory', methods=['POST'])
@validate_schema(CSAFv2Schema)
def create_advisory():
    # Load data
    data = request.get_json() or {}
    # Create and save new advisory
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


@bp.route('/advisory/<int:uid>', methods=['PUT'])
@validate_schema(CSAFv2Schema)
def update_advisory(uid):
    # Load data
    data = request.get_json() or {}
    # Update and save existing advisory
    advisory = Advisory.objects(_id=uid).first()
    if advisory is None: abort(404, 'Advisory not found.')
    advisory.modify(**data)
    advisory.save()
    # Return response
    response = jsonify(advisory.to_json())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_advisory', uid=advisory._id)
    return response


@bp.route('/advisory/<int:uid>', methods=['DELETE'])
def delete_advisory(uid):
    # Delete existing advisory
    advisory = Advisory.objects(_id=uid).first()
    if advisory is None: abort(404, 'Advisory not found.')
    advisory.delete()
    # Return response
    response = jsonify()
    response.status_code = 204
    return response
