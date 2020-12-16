import json, jsonschema

from config import Config


class CSAFv2Schema:
    schema = None

    def __init__(self):
        if CSAFv2Schema.schema is None:
            with open(Config.CSAF_V2_SCHEMA) as file:
                CSAFv2Schema.schema = json.load(file)
        else:
            raise Exception('CSAFv2Schema is a singleton class.')

    @staticmethod
    def validate(data):
        if CSAFv2Schema.schema is None: CSAFv2Schema()
        jsonschema.validate(data, CSAFv2Schema.schema, format_checker=jsonschema.draft7_format_checker)
