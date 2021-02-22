from datetime import datetime
from deepdiff import DeepDiff
from flask import url_for
import math
from mongoengine.queryset import queryset_manager

from app import db


class Base(db.Document):
    meta = {
        'abstract': True
    }
    
    _creation_date = db.ComplexDateTimeField(default=datetime.utcnow)
    _modified_date = db.ComplexDateTimeField(default=datetime.utcnow)
    _accessed_date = db.ComplexDateTimeField(default=datetime.utcnow)

    def __init__(self, init=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if init:
            self.update_timestamps(created=True)

##    @queryset_manager
##    def query(self, q_obj=None, **query):
##        """
##        Use `Base.query` to automatically update all `_accessed_date` timestamps. If this is not
##        desired, use `Base.objects`.
##        """
##        import IPython; IPython.embed()
##        for result in queryset: result.update_timestamps(modified=False)
##        return queryset

##    def update_version(self, **update):
##        old = self.to_json(include_metadata=False)
##        new = self.__class__(**update).to_json(include_metadata=False)
##        diff = DeepDiff(old, new, ignore_order=True, report_repetition=True)
##        if diff:
##            # TODO: Store diff
##            print('Diff:', diff)
##            self._version += 1
##            self.save()
            
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
                    '_id': str(self.id),
                    '_creation_date': '{}Z'.format(self._creation_date.isoformat('T')),
                    '_modified_date': '{}Z'.format(self._modified_date.isoformat('T')),
                    '_accessed_date': '{}Z'.format(self._accessed_date.isoformat('T'))
                }
            )
        return result

    @classmethod
    def get(cls, oid):
        try:
            result = cls.objects(id=oid).first()
        except:
            result = None
        if result: result.update_timestamps(modified=False)
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
        return '<Base "{}">'.format('TODO: self.id')
