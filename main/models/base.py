from main import db

from . import default_date_now


class BaseModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    created = db.Column(db.DateTime(), default=default_date_now)
    modified = db.Column(
        db.DateTime(), default=default_date_now, onupdate=default_date_now
    )
