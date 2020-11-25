from app import db
from app.models import JsonEncodedDict


class ScoreModel(db.Model):
    score = db.Column(JsonEncodedDict)

    def __repr__(self):
        return '<Score "{}">'.format(self.score)
