from flask import make_response

from main import app, config, db
from main.commons.decorators import require_token, use_request_schema
from main.commons.exceptions import DuplicatedCategoryNameError, Forbidden
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
    if CategoryModel.query_by_name(request_data["name"]):
        raise DuplicatedCategoryNameError()
    # get() -> []
    category = CategoryModel(name=request_data.get("name"), user_id=user.id)
    db.session.add(category)
    db.session.commit()

    return make_response({}, 201)


@app.get("/categories/<int:category_id>")
def get_category_by_id(category_id):
    category = CategoryModel.query.get_or_404(category_id)

    return CategorySchema().jsonify(category)


@app.put("/categories/<int:category_id>")
@require_token
@use_request_schema(CategorySchema)
def update_category(category_id, user, request_data):
    name = request_data.get("name")

    category = CategoryModel.query.get_or_404(category_id)
    if category.user_id != user.id:
        raise Forbidden()

    category_with_same_name = CategoryModel.query_by_name(name)
    if category_with_same_name and category_with_same_name.id != category_id:
        raise DuplicatedCategoryNameError()
    # catch database exception for name duplicate
    category.name = name
    db.session.commit()
    # TODO: remove redundant make_response
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
