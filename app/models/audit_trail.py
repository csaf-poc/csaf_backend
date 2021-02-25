import dictdiffer

from app import db
from app.models import Base

class AuditRecord(Base):
    meta = {
        'collection': 'audit_records'
    }

    _ref = db.ReferenceField(Base)
    _diff = db.ListField()

    def __init__(self, ref=None, old_data=None, new_data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if ref:
            self._ref = ref
            self._version = ref._version
        if not old_data is None and not new_data is None:
            self._diff = list(dictdiffer.diff(old_data, new_data))

    def __repr__(self):
        return '<AuditRecord "{}">'.format(self.id)

    def to_json(self, include_metadata=True):
        result = super().to_json(include_metadata=include_metadata)
        if include_metadata:
            result.update(
                {
                    '_diff': self._diff
                }
            )
        return result


##class AuditRecord(Base):
##    meta = {
##        'collection': 'audit_records'
##    }
##
##    _ref = db.ReferenceField(Base, required=True)
##    _diff = db.DictField()
##
##    def __init__(self, ref, old_data, new_data, *args, **kwargs):
##        super().__init__(_version=ref._version, *args, **kwargs)
##        self._ref = ref
##        self._version = ref._version
##        diff = DeepDiff(old_data, new_data, ignore_order=True, report_repetition=True)
##        self._diff = json.loads(diff.to_json())
##
##    def __repr__(self):
##        return '<AuditRecord "{}">'.format(
##            self._ref.document.get('tracking', {}).get('id', 'Unknown'))
##
##    def to_json(self, include_metadata=True):
##        # TODO
##        print('to_json')
##        return {}


##class NewAuditTrail(db.Document):
##    meta = {
##        'collection': 'new_audit_trails'
##    }
##
##    class NewAuditRecord(Base):
##        meta = {
##            'collection': 'new_audit_trails'
##        }
##
##        _diff = db.DictField()
##        
##
##    _advisory = db.ReferenceField(Base, required=True)
##    _trail = db.ListField(Base)
##
##    def __init__(self, advisory, *args, **kwargs):
##        super().__init__(*args, **kwargs)
##        self._advisory = advisory
##
##    def __repr__(self):
##        return '<AuditTrail "{}">'.format(self._advisory.document.get('tracking', {}).get('id', 'Unknown'))
##
##    def to_json(self, include_metadata=True):
##        result = {}
##        if include_metadata:
##            result.update(
##                {
##                    '_id': str(self.id),
##                    '_advisory': str(self._advisory),
##                    '_trail': self._trail
##                }
##            )
##
##    def log(self, old_data, new_data):
##        diff = DeepDiff(old_data, new_data, ignore_order=True, report_repetition=True)
##        delta = Delta(diff).to_dict()
##        audit_record = NewAuditRecord(_version=self._advisory._version, _diff=delta)


##class AuditTrail(Base):
##    meta = {
##        'collection': 'audit_trails'
##    }
##
##    _ref = db.ReferenceField(Base, required=True)
##    _version = db.IntField(min_value=0, default=0)
##    _trail = db.DictField()
##
##    def __init__(self, ref, old_data, new_data):
##        diff = DeepDiff(old_data, new_data, ignore_order=True, report_repetition=True)
##        trail = Delta(diff).to_dict()
##        super().__init__(init=True, _ref=ref, _version=ref._version, _trail=trail)
##
##    def __repr__(self):
##        return '<AuditTrail "{}:{}">'.format(self._ref, self._version)
