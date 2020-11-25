from datetime import datetime
from flask_sqlalchemy import Model
import json
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.mutable import MutableDict


class JSONEncodedDict(sa.types.TypeDecorator):
    impl = sa.types.UnicodeText

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


JsonEncodedDict = MutableDict.as_mutable(JSONEncodedDict)


class BaseModel(Model):
    @declared_attr
    def _id(cls):
        for base in cls.__mro__[1:-1]:
            if getattr(base, '__table__', None) is not None:
                type = sa.ForeignKey(base.id)
                break
        else:
            type = sa.Integer
        return sa.Column(type, primary_key=True)

    _created = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    _modified = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
            
