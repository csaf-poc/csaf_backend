from app import db
from app.models import Base
from app.models.audit_trail import AuditRecord

class Advisory(Base):
    meta = {
        'collection': 'advisories'
    }

    _audit_trail = db.ListField(db.ReferenceField(AuditRecord))

    document = db.DictField()
    product_tree = db.DictField()
    vulnerabilities = db.ListField()

    def __repr__(self):
        return '<Advisory "{}">'.format(self.document.get('tracking', {}).get('id', 'Unknown'))

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
        
    

##class NewAdvisory(Base):
##    meta = {
##        'collection': 'new_advisories'
##    }
##
##    _audit_trail = db.ListField()
##    
##    document = db.DictField()
##    product_tree = db.DictField()
##    vulnerabilities = db.ListField()
##
##    def __init__(self, *args, **kwargs):
##        super().__init__(*args, **kwargs)
##
##    def __repr__(self):
##        return '<Advisory "{}">'.format(self.document.get('tracking', {}).get('id', 'Unknown'))
##
##    def modify(self, query=None, **update):
##        old = self.save().to_json(include_metadata=False)
##        record = AuditRecord(self, old, update)
##        record.save()
##        self._audit_trail.append(record)
####        import IPython; IPython.embed()
##        self.save()
##        return super().modify(query=query, **update)
##        
##
####    def modify(self, **update):
####        self.save()
####        old = self.to_json(include_metadata=False)
######        result = super().modify(**update)
####        record = AuditRecord(self, old, update)
####        record.save()
####        self._audit_trail.append(record)
######        import IPython; IPython.embed()
####        return super().modify(**update)
##
##    def to_json(self, include_metadata=True):
##        result = super().to_json(include_metadata=include_metadata)
##        if include_metadata:
##            result.update(
##                {
##                    '_audit_trail': self._audit_trail
##                }
##            )
##        result.update(
##            {
##                'document': self.document,
##                'product_tree': self.product_tree,
##                'vulnerabilities': self.vulnerabilities
##            }
##        )
##        return result


##class Advisory(Base):
##    meta = {
##        'collection': 'advisories'
##    }
##    
##    document = db.DictField()
##    product_tree = db.DictField()
##    vulnerabilities = db.ListField()
##
##    # TODO: Save not within __init__()
##    def __init__(self, init=False, **data):
##        super().__init__(init=init, **data)
##        if init:
##            AuditTrail(self, {}, data)
##            NewAuditTrail(_ref=self).save()
##
##    def __repr__(self):
##        return '<Advisory "{}">'.format(self.document.get('tracking', {}).get('id', 'Unknown'))
##
##    def update(self, **data):
##        old = self.to_json(include_metadata=False)
##        super().update(**data)
##        new = self.to_json(include_metadata=False)
##        AuditTrail(self, old, new)
##
##    def delete(self, signal_kwargs=None, **write_concern):
##        old = self.to_json(include_metadata=False)
##        self._version += 1
##        self.save()
##        AuditTrail(self, old, {})
##        super().delete(signal_kwargs=signal_kwargs, **write_concern)
##
##    def to_json(self, include_metadata=True):
##        result = super().to_json(include_metadata=include_metadata)
##        result.update(
##            {
##                'document': self.document,
##                'product_tree': self.product_tree,
##                'vulnerabilities': self.vulnerabilities
##            }
##        )
##        return result
