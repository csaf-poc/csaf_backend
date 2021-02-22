from deepdiff import DeepDiff
import json

from app import db
from app.models import Base

class AuditTrail(Base):
    meta = {
        'collection': 'audit_trails'
    }

    _ref = db.ReferenceField(Base, required=True)
    _version = db.IntField(min_value=0, default=0)
    _trail = db.DictField()

    def __init__(self, ref, data, init=False, *args, **kwargs):
        super().__init__(
            _ref=ref,
            _trail = AuditTrail.get_trail({}, data),
            init = init
        )

    @classmethod
    def get_trail(cls, old_data, new_data):
        trail = DeepDiff(old_data, new_data, ignore_order=True, report_repetition=True).to_json()
        return json.loads(trail)
        
##        super().__init__(
##            _ref=ref,
##            _trail=DeepDiff({}, data, ignore_order=True, report_repetition=True)
##        )
##        import IPython; IPython.embed()

##    def to_json(self, include_metadata=True):
##        result = super().to_json(include_metadata=include_metadata)
##        result.update(
##            {
##                'trail': self._trail
##            }
##        )
##        return result

    def __repr__(self):
        return '<AuditTrail "{}:{}">'.format(self._ref, self._version)
