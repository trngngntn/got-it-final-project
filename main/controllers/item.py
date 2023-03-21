from flask import make_response

from main import app, config, db
from main.commons import http_status as HTTPStatus
from main.commons.decorators import require_token, response_schema
from main.commons.exceptions import DuplicatedItemNameError, Forbidden
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas.base import ParamPageSchema
from main.schemas.item import ItemListSchema, ItemSchema, ItemUpdateSchema


@app.get("/categories/<int:category_id>/items")
@response_schema(ParamPageSchema)
def get_all_items_by_category(category_id, page):
    category = CategoryModel.query.get_or_404(category_id)
    items = category.items.paginate(
        page=page, max_per_page=config.PAGINATION_MAX_ITEMS, error_out=True, count=True
    )
    return ItemListSchema().jsonify(items)


@app.post("/categories/<int:category_id>/items")
@require_token
@response_schema(ItemSchema)
def create_item(category_id, user, **kwargs):
    if ItemModel.query_by_name(kwargs["name"]):
        raise DuplicatedItemNameError()

    item = ItemModel(**kwargs, user_id=user.id, category_id=category_id)
    db.session.add(item)
    db.session.commit()

    return make_response({}, HTTPStatus.CREATED)


@app.get("/categories/<int:category_id>/items/<int:item_id>")
def get_item_by_id(category_id, item_id):
    item = ItemModel.query.filter(
        ItemModel.category_id == category_id,
        ItemModel.id == item_id,
    ).first_or_404()
    return ItemSchema().jsonify(item)


@app.put("/categories/<int:category_id>/items/<int:item_id>")
@require_token
@response_schema(ItemUpdateSchema)
def update_item(category_id, item_id, user, **kwargs):
    item = ItemModel.query.filter(
        ItemModel.category_id == category_id, ItemModel.id == item_id
    ).first_or_404()

    if item.user_id != user.id:
        raise Forbidden()

    if kwargs.get("name"):
        item_with_same_name = ItemModel.query_by_name(kwargs["name"])
        if item_with_same_name and item_with_same_name.id != item_id:
            raise DuplicatedItemNameError()

        item.name = kwargs["name"]

    if kwargs.get("description"):
        item.description = kwargs["description"]

    db.session.commit()

    return make_response({})


@app.delete("/categories/<int:category_id>/items/<int:item_id>")
@require_token
def delete_item(category_id, item_id, user):
    item = ItemModel.query.filter(
        ItemModel.category_id == category_id, ItemModel.id == item_id
    ).first_or_404()

    if item.user_id != user.id:
        raise Forbidden()

    db.session.delete(item)
    db.session.commit()

    return make_response({})
