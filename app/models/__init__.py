from datetime import datetime
from flask import url_for
import math

from app import db


class Base(db.Document):
    meta = {'allow_inheritance': True}
    
    _id = db.SequenceField(primary_key=True)
    _version = db.SequenceField()
    _creation_date = db.DateTimeField()
    _modified_date = db.DateTimeField()
    _accessed_date = db.DateTimeField()

    def update_version(self):
        self._version += 1
        self.save()

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
                    '_version': self._version,
                    '_creation_date': '{}Z'.format(self._creation_date.isoformat('T')),
                    '_modified_date': '{}Z'.format(self._modified_date.isoformat('T')),
                    '_accessed_date': '{}Z'.format(self._accessed_date.isoformat('T'))
                }
            )
        return result

    @classmethod
    def paginate(cls, page, per_page, endpoint, include_metadata=True):
        total_items = cls.objects.count()
        per_page = max(1, min(per_page, total_items))
        total_pages = math.ceil(total_items/per_page)
        page = max(1, min(page, total_pages))

        bases = cls.objects.skip((page-1)* per_page).limit(per_page)
        for base in bases: base.update_timestamps(modified=False)
        result = {
            '_items': [base.to_json(include_metadata=include_metadata) for base in bases],
            '_meta': {
                '_page': page,
                '_per_page': per_page,
                '_total_pages': total_pages,
                '_total_items': total_items
            },
            '_links': {
                '_self': url_for(
                    endpoint,
                    page=page,
                    per_page=per_page
                ),
                '_next': url_for(
                    endpoint,
                    page=page+1,
                    per_page=per_page
                ) if page+1 <= total_pages else None,
                '_prev': url_for(
                    endpoint,
                    page=page-1,
                    per_page=per_page
                ) if page-1 >= 1 else None
            }
        }
        return result

    def __repr__(self):
        return '<Base "{}">'.format(self._id)
