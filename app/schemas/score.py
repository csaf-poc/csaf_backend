import json
import jsonschema
from marshmallow import post_dump, validate, ValidationError

from app import ma
from app.models.score import ScoreModel
from app.schemas import BaseSchema
from config import Config


class ScoreSchema(BaseSchema):
    class Meta:
        model = ScoreModel
    

    products = ma.List(
        ma.Str(
            validate=validate.Length(min=1)
        ),
        required=True,
        allow_none=False,
        validate=validate.Length(min=1)
    )

    def validate_cvss_v2(score):
        with open(Config.CVSS_V2_SCHEMA) as json_file:
            cvss_v2_schema = json.load(json_file)
        try:
            jsonschema.validate(score, cvss_v2_schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(e.message)
    
    cvss_v2 = ma.Dict(
        allow_none=True,
        validate=validate_cvss_v2
    )

    def validate_cvss_v3(score):
        version = score.get('version')
        # CVSSv3.0
        if version == "3.0":
            with open(Config.CVSS_V3_0_SCHEMA) as json_file:
                cvss_v3_0_schema = json.load(json_file)
            try:
                jsonschema.validate(score, cvss_v3_0_schema)
            except jsonschema.exceptions.ValidationError as e:
                raise ValidationError(e.message)
        # CVSSv3.1
        elif version == "3.1":
            with open(Config.CVSS_V3_1_SCHEMA) as json_file:
                cvss_v3_1_schema = json.load(json_file)
            try:
                jsonschema.validate(score, cvss_v3_1_schema)
            except jsonschema.exceptions.ValidationError as e:
                raise ValidationError(e.message)
        else:
            raise ValidationError("'version' is not one of ['3.0', '3.1']")
    
    cvss_v3 = ma.Dict(
        allow_none=True,
        validate=validate_cvss_v3
    )

    @post_dump(pass_original=True)
    def post_dumping(self, data, original_data, **kwargs):
        data.update(original_data.score)
        return data
    

class ScoreUpdateSchema(ScoreSchema):
    
    products = ma.List(
        ma.Str(
            validate=validate.Length(min=1)
        ),
        allow_none=False,
        validate=validate.Length(min=1)
    )
