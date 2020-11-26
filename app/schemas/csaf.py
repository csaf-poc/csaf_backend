import json
import jsonschema

class CsafSchema:

    def __init__(self, json_schema):
        with open(json_schema) as json_file:
            self.schema = json.load(json_file)

    def validate(self, data):
        jsonschema.validate(data, self.schema)
