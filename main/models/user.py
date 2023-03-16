from main import db

from . import default_date_now


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    salt = db.Column(db.String(16), nullable=False)
    created = db.Column(db.DateTime(), default=default_date_now)
    modified = db.Column(
        db.DateTime(), default=default_date_now, onupdate=default_date_now
    )

    @classmethod
    def query_by_email(cls, email: str):
        return cls.query.filter(cls.email == email).first()
