from app import ma
from app.models import BaseModel


class BaseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = BaseModel

    _id = ma.Integer(dump_only=True)
    _created = ma.DateTime(dump_only=True)
    _modified = ma.DateTime(dump_only=True)
