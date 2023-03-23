from datetime import datetime

from main import db


class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(
        db.Integer(), db.ForeignKey("users.id"), unique=False, nullable=False
    )
    items = db.relationship(
        "ItemModel", back_populates="category", lazy="dynamic", cascade="all, delete"
    )
    created = db.Column(db.DateTime(), default=datetime.now)
    modified = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
