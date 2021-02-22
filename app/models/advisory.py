from app import db
from app.models import Base


from app.models.audit_trail import AuditTrail

class Advisory(Base):
    meta = {
        'collection': 'advisories'
    }
    
    document = db.DictField()
    product_tree = db.DictField()
    vulnerabilities = db.ListField()

    def __init__(self, init=False, **data):
        super().__init__(init=init, **data)
        if init:
            AuditTrail(self, data, init=init)

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

    def __repr__(self):
        return '<Advisory "{}">'.format(self.document.get('tracking', {}).get('id', 'Unknown'))
