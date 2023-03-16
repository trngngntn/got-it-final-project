from flask import abort, make_response, request

from main import app, db
from main.commons import http_status as HTTPStatus
from main.commons import params
from main.commons.decorators import paginate, require_token
from main.commons.exceptions import DuplicatedItemNameError
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas.base import make_pagination_schema
from main.schemas.item import ItemSchema, ItemUpdateSchema


@app.get("/categories/<int:category_id>/items")
@paginate
def get_all_item_by_category(category_id, page):
    category = CategoryModel.query.get_or_404(category_id)
    items = category.items.paginate(
        page=page, max_per_page=params.PAGINATE_MAX_ITEMS, error_out=True, count=True
    )
    data = make_pagination_schema(ItemSchema).jsonify(items)
    return make_response(data)


@app.post("/categories/<int:category_id>/items")
@require_token
def create_item(category_id, jwt):
    data = ItemSchema().loads(request.get_data())
    if ItemModel.query_by_name(data["name"]):
        raise DuplicatedItemNameError()

    item = ItemModel(**data, user_id=jwt.get("uid"), category_id=category_id)
    db.session.add(item)
    db.session.commit()

    return make_response({}, HTTPStatus.CREATED)


@app.get("/categories/<int:category_id>/items/<int:item_id>")
def get_item_by_id(category_id, item_id):
    item = ItemModel.query.filter(
        ItemModel.category_id == category_id, ItemModel.id == item_id
    ).first_or_404()
    item = ItemSchema().jsonify(item)
    return make_response(item)


@app.put("/categories/<int:category_id>/items/<int:item_id>")
@require_token
def update_item(category_id, item_id, jwt):
    item = ItemModel.query.filter(
        ItemModel.category_id == category_id, ItemModel.id == item_id
    ).first_or_404()

    if item.user_id != jwt.get("uid"):
        abort(HTTPStatus.FORBIDDEN)

    item_data = ItemUpdateSchema().loads(request.get_data())

    if item_data.get("name"):
        item_with_same_name = ItemModel.query_by_name(item_data["name"])
        if item_with_same_name and item_with_same_name.id != item_id:
            raise DuplicatedItemNameError()

        item.name = item_data["name"]

    if item_data.get("description"):
        item.description = item_data["description"]

    db.session.commit()

    return make_response({})


@app.delete("/categories/<int:category_id>/items/<int:item_id>")
@require_token
def delete_item(category_id, item_id, jwt):
    item = ItemModel.query.filter(
        ItemModel.category_id == category_id, ItemModel.id == item_id
    ).first_or_404()

    if item.user_id != jwt.get("uid"):
        abort(HTTPStatus.FORBIDDEN)

    db.session.delete(item)
    db.session.commit()

    return make_response({})
