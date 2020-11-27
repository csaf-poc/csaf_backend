from app import db
from app.models import Base


class Advisory(Base):
    document = db.DictField()
    product_tree = db.DictField()
    vulnerabilities = db.ListField()

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
