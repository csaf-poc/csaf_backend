from flask import abort, jsonify, request, url_for
from mongoengine.queryset.visitor import Q

from app.api import bp
from app.api import validate_schema
from app.models.advisory import Advisory
from app.models.audit_trail import AuditRecord
from app.schemas.csaf import CSAFv2Schema
from app.schemas.filter import FilterSchema


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
                default: 1
        -   name: per_page
            in: query
            required: false
            schema:
                type: integer
                default: 10
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
                default: 1
        -   name: per_page
            in: query
            required: false
            schema:
                type: integer
                default: 10
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
        -   name: document
            in: body
            required: true
            schema:
                type: object
                default: {}
                example: {
                    "document":{
                        "csaf_version":"2.0",
                        "title":"Minimal Advisory",
                        "publisher":{
                            "type":"discoverer"
                        },
                        "type":"Example",
                        "tracking":{
                            "current_release_date":"2020-12-31T00:00:00Z",
                            "id":"Example Document",
                            "initial_release_date":"2020-12-31T00:00:00Z",
                            "revision_history":[
                                {
                                    "number":"1",
                                    "date":"2020-12-31T00:00:00Z",
                                    "summary":"Summary of Example Advisory"
                                }
                            ],
                            "status":"draft",
                            "version":"1"
                        }
                    }
                }
    responses:
        201:
            description: Advisory created.
        5xx:
            description: Server error.
    """
    # Load data
    data = request.get_json() or {}
    # Create advisory
    advisory = Advisory()
    advisory.initialize(**data)
    # Return response
    response = jsonify(advisory.to_json())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_advisory', uid=str(advisory.id))
    return response


@bp.route('/advisories/<string:uid>', methods=['GET'])
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
                type: string
    responses:
        200:
            description: Advisory with ID `uid`.
        404:
            description: Advisory with ID `uid` not found.
        5xx:
            description: Server error.
    """
    # Get existing advisory
    advisory = Advisory.get(uid)
    if advisory is None: abort(404, 'Advisory not found.')
    response = jsonify(advisory.to_json(include_metadata=include_metadata))
    response.status_code = 200
    return response


@bp.route('/advisories/<string:uid>/export', methods=['GET'])
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
                type: string
    responses:
        200:
            description: Advisory with ID `uid`.
        404:
            description: Advisory with ID `uid` not found.
        5xx:
            description: Server error.
    """
    return get_advisory(uid, include_metadata=False)


@bp.route('/advisories/<string:uid>', methods=['PUT'])
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
                type: string
        -   name: advisory
            in: body
            required: true
            schema:
                type: object
                default: {}
                example: {
                    "document":{
                        "csaf_version":"2.0",
                        "title":"Minimal Advisory",
                        "publisher":{
                            "type":"discoverer"
                        },
                        "type":"Example",
                        "tracking":{
                            "current_release_date":"2020-12-31T00:00:00Z",
                            "id":"Example Document",
                            "initial_release_date":"2020-12-31T00:00:00Z",
                            "revision_history":[
                                {
                                    "number":"1",
                                    "date":"2020-12-31T00:00:00Z",
                                    "summary":"Summary of Example Advisory"
                                }
                            ],
                            "status":"draft",
                            "version":"1"
                        }
                    }
                }
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
    # Get existing advisory
    advisory = Advisory.get(uid)
    if advisory is None: abort(404, 'Advisory not found.')
    # Update advisory
    advisory.modify(**data)
    # Return response
    response = jsonify(advisory.to_json())
    response.status_code = 200
    response.headers['Location'] = url_for('api.get_advisory', uid=str(advisory.id))
    return response


@bp.route('/advisories/<string:uid>', methods=['DELETE'])
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
                type: string
    responses:
        204:
            description: Advisory with ID `uid` deleted.
        404:
            description: Advisory with ID `uid` not found.
        5xx:
            description: Server error.
    """
    # Get existing advisory
    advisory = Advisory.get(uid)
    if advisory is None: abort(404, 'Advisory not found.')
    # Delete advisory
    advisory.delete()
    # Return response
    response = jsonify()
    response.status_code = 204
    return response


@bp.route('/advisories/search', methods=['POST'])
@validate_schema(FilterSchema)
def search_advisories(include_metadata=True):
    """
    Search advisories matching filtering criteria.
    ---
    tags:
        - advisories
    parameters:
        -   name: limit
            in: query
            required: false
            schema:
                type: integer
                default: 10
                minimum: 1
                maximum: 1000
        -   name: filters
            in: body
            required: true
            schema:
                type: object
                default: {}
                example: {
                    "filters": [
                        {
                            "field": "document__title",
                            "op": "icontains",
                            "value": "Document Title"
                        }
                    ],
                    "op": "and"
                }
    responses:
        200:
            description: Matching advisories.
        5xx:
            description: Server error.
    """
    # Load data
    data = request.get_json() or {}
    filters = data.get('filters') or []
    operator = data.get('op') or 'and'
    # Build query
    query = Q()
    for f in filters:
        q = {'{}__{}'.format(f['field'].lstrip('_'), f['op']): f['value']}
        if operator == 'or':
            query = query | Q(**q)
        else:
            query = query & Q(**q)
    # Query objects
    limit = request.args.get('limit', 10, type=int)
    limit = max(1, min(limit, 1000))
    advisories = Advisory.search(query, limit)
    result = {
        '_items': [advisory.to_json(include_metadata=include_metadata) for advisory in advisories]
    }
    # Return response
    response = jsonify(result)
    response.status_code = 200
    return response


@bp.route('/advisories/<string:uid>/trail', methods=['GET'])
def audit_trail(uid, include_metadata=True):
    """
    Get audit trail of advisory with ID `uid`.
    ---
    tags:
        - advisories
    parameters:
        -   name: uid
            in: path
            required: true
            schema:
                type: string
    responses:
        200:
            description: Audit trail of advisory with ID `uid`.
        404:
            description: Advisory with ID `uid` not found.
        5xx:
            description: Server error.
    """
    # Get audit trail of advisory
    audit_records = AuditRecord.get(uid)
    if len(audit_records) <= 0: abort(404, 'Advisory not found.')
    result = {
        '_items': [audit_record.to_json(include_metadata=include_metadata) for audit_record in audit_records]
    }
    # Return response
    response = jsonify(result)
    response.status_code = 200
    return response
