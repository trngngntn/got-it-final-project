from datetime import datetime

from main import db


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
    created = db.Column(db.DateTime(), default=datetime.now)
    modified = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    @classmethod
    def query_by_name(cls, name: str):
        return cls.query.filter(cls.name == name).first()
