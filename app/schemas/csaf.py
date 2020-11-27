import jsonschema

from app.schemas import AbstractJsonSchema
from config import Config


class CSAFv2Schema(AbstractJsonSchema):

    @staticmethod
    def validate(data):
        if CSAFv2Schema.schema is None:
            CSAFv2Schema(Config.CSAF_V2_SCHEMA)
        jsonschema.validate(data, CSAFv2Schema.schema)
