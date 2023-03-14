from base import BaseModel

from main import db


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    name = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(
        db.Integer(), db.ForeignKey("users.id"), unique=False, nullable=False
    )
    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete"
    )
