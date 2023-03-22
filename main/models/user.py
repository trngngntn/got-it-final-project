from datetime import datetime

from main import db
from main.commons import const


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(const.FIELD_EMAIL_MAX_LEN), unique=True, nullable=False)
    password = db.Column(db.String(const.HASHED_PASSWORD_LEN), nullable=False)
    salt = db.Column(db.String(const.SALT_HEX_LEN), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.now)
    modified = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    @classmethod
    def query_by_email(cls, email: str):
        return cls.query.filter(cls.email == email).first()
