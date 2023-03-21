from flask import make_response

from main import app, config, db
from main.commons import http_status as HTTPStatus
from main.commons.decorators import require_token, response_schema
from main.commons.exceptions import DuplicatedCategoryNameError, Forbidden
from main.models.category import CategoryModel
from main.schemas.base import ParamPageSchema
from main.schemas.category import CategoryListSchema, CategorySchema


@app.get("/categories")
@response_schema(ParamPageSchema)
def get_all_categories(page):
    categories = CategoryModel.query.paginate(
        page=page, max_per_page=config.PAGINATION_MAX_ITEMS, error_out=True, count=True
    )
    return CategoryListSchema().jsonify(categories)


@app.post("/categories")
@require_token
@response_schema(CategorySchema)
def create_category(user, name):
    if CategoryModel.query_by_name(name):
        raise DuplicatedCategoryNameError()

    category = CategoryModel(name=name, user_id=user.id)
    db.session.add(category)
    db.session.commit()

    return make_response({}, HTTPStatus.CREATED)


@app.get("/categories/<int:category_id>")
def get_category_by_id(category_id):
    category = CategoryModel.query.get_or_404(category_id)

    return CategorySchema().jsonify(category)


@app.put("/categories/<int:category_id>")
@require_token
@response_schema(CategorySchema)
def update_category(category_id, name, user):
    category = CategoryModel.query.get_or_404(category_id)
    if category.user_id != user.id:
        raise Forbidden()

    category_with_same_name = CategoryModel.query_by_name(name)
    if category_with_same_name and category_with_same_name.id != category_id:
        raise DuplicatedCategoryNameError()

    category.name = name
    db.session.commit()

    return make_response({})


@app.delete("/categories/<int:category_id>")
@require_token
def delete_category(category_id, user):
    category = CategoryModel.query.get_or_404(category_id)

    if category.user_id != user.id:
        raise Forbidden()

    db.session.delete(category)
    db.session.commit()

    return make_response({})
