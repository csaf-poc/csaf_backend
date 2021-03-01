from app import db
from app.models import Base
from app.models.audit_trail import AuditRecord

class Advisory(Base):
    meta = {
        'collection': 'advisories'
    }

    _audit_records = db.ListField(db.ReferenceField(AuditRecord))

    document = db.DictField()
    product_tree = db.DictField()
    vulnerabilities = db.ListField()

    def __repr__(self):
        return '<Advisory "{}">'.format(self.document.get('tracking', {}).get('id', 'Unknown'))

    def initialize(self, **data):
        # Save initial advisory
        initial_data = self.save().to_json(include_metadata=False)
        # Create and save new audit record
        audit_record = AuditRecord(self, initial_data, initial_data).save()
        # Link audit record to advisory
        self._audit_records.append(audit_record)
        self.save()
        # Update advisory
        self.modify(**data)

    def modify(self, query=None, **update):
        # Modify advisory
        old_data = self.to_json(include_metadata=False)
        result = super().modify(query=query, **update)
        new_data = self.to_json(include_metadata=False)
        # Create and save new audit record
        audit_record = AuditRecord(self, old_data, new_data).save()
        # Link audit record to advisory
        self._audit_records.append(audit_record)
        self.save()
        return result

    def delete(self, signal_kwargs=None, **write_concern):
        old_data = self.to_json(include_metadata=False)
        super().delete(signal_kwargs=signal_kwargs, **write_concern)
        audit_record = AuditRecord(self, old_data, {})
        audit_record.save()

    def to_json(self, include_metadata=True):
        result = super().to_json(include_metadata=include_metadata)
        result.update(
            {
                'document': self.document,
                'product_tree': self.product_tree,
                'vulnerabilities': self.vulnerabilities
            }
        )
        return result
