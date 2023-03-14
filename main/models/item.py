from base import BaseModel

from main import db


class ItemModel(BaseModel):
    __tablename__ = "items"

    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(), nullable=False)
    user_id = db.Column(
        db.Integer(), db.ForeignKey("users.id"), unique=False, nullable=False
    )
    category_id = db.Column(
        db.Integer(), db.ForeignKey("categories.id"), unique=False, nullable=False
    )
    category = db.relationship("CategoryModel", back_populates="items")
