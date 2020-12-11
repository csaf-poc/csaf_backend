import json, jsonschema


class FilterSchema:
    schema = None

    def __init__(self):
        if FilterSchema.schema is None:
            with open('app/schemas/filter_schema.json') as file:
                FilterSchema.schema = json.load(file)
        else:
            raise Exception('FilterSchema is a singleton class.')

    @staticmethod
    def validate(data):
        if FilterSchema.schema is None: FilterSchema()
        jsonschema.validate(data, FilterSchema.schema)
