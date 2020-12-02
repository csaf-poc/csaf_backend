from flask import abort, jsonify, request, url_for

from app.api import bp
from app.api import validate_schema
from app.models.advisory import Advisory
from app.schemas.csaf import CSAFv2Schema


@bp.route('/advisories', methods=['GET'])
def list_advisories(endpoint='api.list_advisories', include_metadata=True):
    """
    List advisories.
    ---
    tags:
        - advisories
    parameters:
        -   name: page
            in: query
            required: false
            schema:
                type: integer
        -   name: per_page
            in: query
            required: false
            schema:
                type: integer
    responses:
        200:
            description: Advisories
        5xx:
            description: Server error.
    """
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
    """
    Export advisories in CSAF format.
    ---
    tags:
        - advisories
    parameters:
        -   name: page
            in: query
            required: false
            schema:
                type: integer
        -   name: per_page
            in: query
            required: false
            schema:
                type: integer
    responses:
        200:
            description: Advisories
        5xx:
            description: Server error.
    """
    return list_advisories(endpoint=endpoint, include_metadata=False)


@bp.route('/advisories', methods=['POST'])
@validate_schema(CSAFv2Schema)
def create_advisory():
    """
    Create a new advisory.
    ---
    tags:
        - advisories
    parameters:
        -   name: advisory
            in: body
            required: true
            schema:
                type: object
    responses:
        201:
            description: Advisory created.
        5xx:
            description: Server error.
    """
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
    """
    Get advisory with ID `uid`.
    ---
    tags:
        - advisories
    parameters:
        -   name: uid
            in: path
            required: true
            schema:
                type: integer
    responses:
        200:
            description: Advisory with ID `uid`.
        404:
            description: Advisory with ID `uid` not found.
        5xx:
            description: Server error.
    """
    # Get existing advisory
    advisory = Advisory.objects(_id=uid).first()
    if advisory is None: abort(404, 'Advisory not found.')
    advisory.update_timestamps(modified=False)
    response = jsonify(advisory.to_json(include_metadata=include_metadata))
    response.status_code = 200
    return response


@bp.route('/advisories/<int:uid>/export', methods=['GET'])
def export_advisory(uid):
    """
    Export advisory with ID `uid` in CSAF format.
    ---
    tags:
        - advisories
    parameters:
        -   name: uid
            in: path
            required: true
            schema:
                type: integer
    responses:
        200:
            description: Advisory with ID `uid`.
        404:
            description: Advisory with ID `uid` not found.
        5xx:
            description: Server error.
    """
    return get_advisory(uid, include_metadata=False)


@bp.route('/advisories/<int:uid>', methods=['PUT'])
@validate_schema(CSAFv2Schema)
def update_advisory(uid):
    """
    Update advisory with ID `uid`.
    ---
    tags:
        - advisories
    parameters:
        -   name: uid
            in: path
            required: true
            schema:
                type: integer
        -   name: advisory
            in: body
            required: true
            schema:
                type: object
    responses:
        200:
            description: Advisory with ID `uid`.
        404:
            description: Advisory with ID `uid` not found.
        5xx:
            description: Server error.
    """
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
    """
    Delete advisory with ID `uid`.
    ---
    tags:
        - advisories
    parameters:
        -   name: uid
            in: path
            required: true
            schema:
                type: integer
    responses:
        204:
            description: Advisory with ID `uid` deleted.
        404:
            description: Advisory with ID `uid` not found.
        5xx:
            description: Server error.
    """
    # Delete existing advisory
    advisory = Advisory.objects(_id=uid).first()
    if advisory is None: abort(404, 'Advisory not found.')
    advisory.delete()
    # Return response
    response = jsonify()
    response.status_code = 204
    return response


@bp.route('/advisories/search', methods=['GET'])
def search_advisories(include_metadata=True):
    """
    Search advisories.
    ---
    tags:
        - advisories
    parameters:
        -   name: document_title
            in: query
            required: false
            schema:
                type: string
        -   name: document_type
            in: query
            required: false
            schema:
                type: string
    responses:
        200:
            description: First matching advisory.
        404:
            description: No matching advisory found.
        5xx:
            description: Server error.
    """
    document_title = request.args.get('document_title', None, type=str)
    q_document_title = Q(document__title__icontains=document_title)
    document_type = request.args.get('document_type', None, type=str)
    q_document_type = Q(document__type__iexact=document_type)
    # TODO: Return paginated response
    advisory = Advisory.objects.filter(q_document_title or q_document_type).first()
    if advisory is None: abort(404, 'No matching advisory found.')
    advisory.update_timestamps(modified=False)
    # Return response
    response = jsonify(advisory.to_json(include_metadata=include_metadata))
    response.status_code = 200
    return response
