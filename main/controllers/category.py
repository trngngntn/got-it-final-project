from flask import abort, make_response, request

from main import app, db
from main.commons import http_status as HTTPStatus
from main.commons import params
from main.commons.decorators import paginate, require_token
from main.commons.exceptions import DuplicatedCategoryNameError
from main.models.category import CategoryModel
from main.schemas.base import make_pagination_schema
from main.schemas.category import CategorySchema


@app.get("/categories")
@paginate
def get_all_categories(page):
    categories = CategoryModel.query.paginate(
        page=page, max_per_page=params.PAGINATE_MAX_ITEMS, error_out=True, count=True
    )
    data = make_pagination_schema(CategorySchema).jsonify(categories)
    return make_response(data)


@app.post("/categories")
@require_token
def create_category(jwt):
    data = CategorySchema().loads(request.get_data())
    if CategoryModel.query_by_name(data["name"]):
        raise DuplicatedCategoryNameError()

    category = CategoryModel(**data, user_id=jwt.get("uid"))
    db.session.add(category)
    db.session.commit()

    return make_response({}, HTTPStatus.CREATED)


@app.get("/categories/<int:category_id>")
def get_category_by_id(category_id):
    category = CategoryModel.query.get_or_404(category_id)
    category = CategorySchema().jsonify(category)

    return make_response(category)


@app.put("/categories/<int:category_id>")
@require_token
def update_category(category_id, jwt):
    category = CategoryModel.query.get_or_404(category_id)
    if category.user_id != jwt.get("uid"):
        abort(HTTPStatus.FORBIDDEN)

    data = CategorySchema().loads(request.get_data())

    category_with_same_name = CategoryModel.query_by_name(data["name"])
    if category_with_same_name and category_with_same_name.id == category_id:
        raise DuplicatedCategoryNameError()

    category.name = data["name"]
    db.session.commit()

    return make_response({})


@app.delete("/categories/<int:category_id>")
@require_token
def delete_category(category_id, jwt):
    category = CategoryModel.query.get_or_404(category_id)

    if category.user_id != jwt.get("uid"):
        abort(HTTPStatus.FORBIDDEN)

    db.session.delete(category)
    db.session.commit()

    return make_response({})
