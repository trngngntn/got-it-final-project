from sqlalchemy.exc import IntegrityError

from main import app, config, db
from main.commons.decorators import require_token, use_request_schema
from main.commons.exceptions import (
    DuplicatedCategoryNameError,
    Forbidden,
    is_duplicated_entry_error,
)
from main.models.category import CategoryModel
from main.schemas.base import ParamPageSchema
from main.schemas.category import CategoryListSchema, CategorySchema


@app.get("/categories")
@use_request_schema(ParamPageSchema)
def get_all_categories(request_data):
    categories = CategoryModel.query.paginate(
        page=request_data["page"],
        max_per_page=config.PAGINATION_MAX_ITEMS,
    )
    return CategoryListSchema().jsonify(categories)


@app.post("/categories")
@require_token
@use_request_schema(CategorySchema)
def create_category(user, request_data):
    category = CategoryModel(name=request_data["name"], user_id=user.id)
    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError as e:
        if is_duplicated_entry_error(e):
            raise DuplicatedCategoryNameError()
        else:
            raise e
    return {}, 201


@app.get("/categories/<int:category_id>")
def get_category_by_id(category_id):
    category = CategoryModel.query.get_or_404(category_id)

    return CategorySchema().jsonify(category)


@app.put("/categories/<int:category_id>")
@require_token
@use_request_schema(CategorySchema)
def update_category(category_id, user, request_data):
    name = request_data["name"]

    category = CategoryModel.query.get_or_404(category_id)
    if category.user_id != user.id:
        raise Forbidden()

    category.name = name

    try:
        db.session.commit()
    except IntegrityError as e:
        if is_duplicated_entry_error(e):
            raise DuplicatedCategoryNameError()
        else:
            raise e

    return {}


@app.delete("/categories/<int:category_id>")
@require_token
def delete_category(category_id, user):
    category = CategoryModel.query.get_or_404(category_id)

    if category.user_id != user.id:
        raise Forbidden()

    db.session.delete(category)
    db.session.commit()

    return {}
