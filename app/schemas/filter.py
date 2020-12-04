import jsonschema

from app.schemas import AbstractJsonSchema

class FilterSchema(AbstractJsonSchema):

    @staticmethod
    def validate(data):
        if FilterSchema.schema is None:
            FilterSchema('app/schemas/filter_schema.json')
        jsonschema.validate(data, FilterSchema.schema)
