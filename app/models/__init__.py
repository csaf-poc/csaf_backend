from datetime import datetime
from app import db


class Base(db.Document):
    meta = {'allow_inheritance': True}
    
    _id = db.SequenceField(primary_key=True)
    _creation_date = db.DateTimeField()
    _modified_date = db.DateTimeField()

    def save(self, *args, **kwargs):
        timestamp = datetime.utcnow()
        if not self._creation_date:
            self._creation_date = timestamp
        self._modified_date = timestamp
        return super().save(*args, **kwargs)

    def to_dict(self, include_metadata=True):
        result = {}
        if include_metadata:
            result.update(
                {
                    '_id': self._id,
                    '_creation_date': '{}Z'.format(self._creation_date.isoformat('T')),
                    '_modified_date': '{}Z'.format(self._modified_date.isoformat('T'))
                }
            )
        return result

    def __repr__(self):
        return '<Base "{}">'.format(self._id)
