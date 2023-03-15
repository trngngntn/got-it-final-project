from main import db

from . import default_date_now


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(
        db.Integer(), db.ForeignKey("users.id"), unique=False, nullable=False
    )
    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete"
    )
    created = db.Column(db.DateTime(), default=default_date_now)
    modified = db.Column(
        db.DateTime(), default=default_date_now, onupdate=default_date_now
    )
