from datetime import datetime
from app import db


class Base(db.Document):
    meta = {'allow_inheritance': True}
    
    _id = db.SequenceField(primary_key=True)
    _creation_date = db.DateTimeField()
    _modified_date = db.DateTimeField()
    _accessed_date = db.DateTimeField()

    def update_timestamps(self, created=False, modified=True, accessed=True):
        timestamp = datetime.utcnow()
        if created:
            self._creation_date = timestamp
        if modified:
            self._modified_date = timestamp
        if accessed:
            self._accessed_date = timestamp
        self.save()

    def to_json(self, include_metadata=True):
        result = {}
        if include_metadata:
            result.update(
                {
                    '_id': self._id,
                    '_creation_date': '{}Z'.format(self._creation_date.isoformat('T')),
                    '_modified_date': '{}Z'.format(self._modified_date.isoformat('T')),
                    '_accessed_date': '{}Z'.format(self._accessed_date.isoformat('T'))
                }
            )
        return result

    def __repr__(self):
        return '<Base "{}">'.format(self._id)
