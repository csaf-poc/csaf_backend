from flask import abort, jsonify, request, url_for

from app.api import bp
from app.api import validate_schema
from app.models.advisory import Advisory
from app.schemas.csaf import CSAFv2Schema


@bp.route('/advisories', methods=['GET'])
def list_advisories(endpoint='api.list_advisories', include_metadata=True):
    # List advisories
    per_page = request.args.get('per_page', 10, type=int)
    page = request.args.get('page', 1, type=int)
    pagination = Advisory.paginate(page, per_page, endpoint, include_metadata=include_metadata)
    # Return response
    response = jsonify(pagination)
    response.status_code = 200
    return response

@bp.route('/advisories/export', methods=['GET'])
def export_advisories(endpoint='api.export_advisories'):
    return list_advisories(endpoint=endpoint, include_metadata=False)


@bp.route('/advisories', methods=['POST'])
@validate_schema(CSAFv2Schema)
def create_advisory():
    # Load data
    data = request.get_json() or {}
    # Create new advisory
    advisory = Advisory(**data)
    advisory.update_timestamps(created=True)
    # Return response
    response = jsonify(advisory.to_json())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_advisory', uid=advisory._id)
    return response


@bp.route('/advisories/<int:uid>', methods=['GET'])
def get_advisory(uid, include_metadata=True):
    # Get existing advisory
    advisory = Advisory.objects(_id=uid).first()
    if advisory is None: abort(404, 'Advisory not found.')
    advisory.update_timestamps(modified=False)
    response = jsonify(advisory.to_json(include_metadata=include_metadata))
    response.status_code = 200
    return response


@bp.route('/advisories/<int:uid>/export', methods=['GET'])
def export_advisory(uid):
    return get_advisory(uid, include_metadata=False)


@bp.route('/advisories/<int:uid>', methods=['PUT'])
@validate_schema(CSAFv2Schema)
def update_advisory(uid):
    # Load data
    data = request.get_json() or {}
    # Update existing advisory
    advisory = Advisory.objects(_id=uid).first()
    if advisory is None: abort(404, 'Advisory not found.')
    advisory.modify(**data)
    advisory.update_timestamps()
    # Return response
    response = jsonify(advisory.to_json())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_advisory', uid=advisory._id)
    return response


@bp.route('/advisories/<int:uid>', methods=['DELETE'])
def delete_advisory(uid):
    # Delete existing advisory
    advisory = Advisory.objects(_id=uid).first()
    if advisory is None: abort(404, 'Advisory not found.')
    advisory.delete()
    # Return response
    response = jsonify()
    response.status_code = 204
    return response
