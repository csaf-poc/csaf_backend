import dictdiffer

from app import db
from app.models import Base

class AuditRecord(Base):
    meta = {
        'collection': 'audit_records'
    }

    _ref = db.StringField()
    _diff = db.ListField()

    def __init__(self, ref=None, old_data=None, new_data=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if ref:
            self._ref = str(ref.id)
            self._version = ref._version
        if not old_data is None and not new_data is None:
            self._diff = list(dictdiffer.diff(old_data, new_data))

    def __repr__(self):
        return '<AuditRecord "{}">'.format(self.id)

    @classmethod
    def get(cls, oid):
        audit_records = cls.objects(_ref=oid)
        for audit_record in audit_records:
            audit_record._update_timestamps(modified=False)
        return audit_records

    def to_json(self, include_metadata=True):
        result = super().to_json(include_metadata=include_metadata)
        if include_metadata:
            result.update(
                {
                    '_ref': self._ref,
                    '_diff': self._diff
                }
            )
        return result
