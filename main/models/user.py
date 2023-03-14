from base import BaseModel

from main import db


class UserModel(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(254), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    salt = db.Column(db.String(16), nullable=False)
