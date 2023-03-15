from main import db

from . import default_date_now


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(), nullable=False)
    user_id = db.Column(
        db.Integer(), db.ForeignKey("users.id"), unique=False, nullable=False
    )
    category_id = db.Column(
        db.Integer(), db.ForeignKey("categories.id"), unique=False, nullable=False
    )
    category = db.relationship("CategoryModel", back_populates="items")
    created = db.Column(db.DateTime(), default=default_date_now)
    modified = db.Column(
        db.DateTime(), default=default_date_now, onupdate=default_date_now
    )
