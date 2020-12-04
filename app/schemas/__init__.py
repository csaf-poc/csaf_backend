from abc import ABC, abstractmethod
import json


class AbstractJsonSchema(ABC):
    schema = None

    def __init__(self, json_file):
        if AbstractJsonSchema.schema is None:
            with open(json_file) as file:
                AbstractJsonSchema.schema = json.load(file)
        else:
            raise Exception('AbstractJsonSchema is a singleton class.')

    @abstractmethod
    def validate(self, data):
        pass
