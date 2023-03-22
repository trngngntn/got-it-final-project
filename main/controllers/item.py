from main import app, config, db
from main.commons.decorators import get_item, require_token, use_request_schema
from main.commons.exceptions import DuplicatedItemNameError, Forbidden
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas.base import ParamPageSchema
from main.schemas.item import ItemListSchema, ItemSchema, ItemUpdateSchema


@app.get("/categories/<int:category_id>/items")
@use_request_schema(ParamPageSchema)
def get_all_items_by_category(category_id, request_data):
    page = request_data["page"]
    category = CategoryModel.query.get_or_404(category_id)
    items = category.items.paginate(
        page=page,
        max_per_page=config.PAGINATION_MAX_ITEMS,
    )
    return ItemListSchema().jsonify(items)


@app.post("/categories/<int:category_id>/items")
@require_token
@use_request_schema(ItemSchema)
def create_item(category_id, user, request_data):
    CategoryModel.query.get_or_404(category_id)

    if ItemModel.query_by_name(request_data["name"]):
        raise DuplicatedItemNameError()

    item = ItemModel(**request_data, user_id=user.id, category_id=category_id)
    db.session.add(item)
    db.session.commit()

    return {}, 201


@app.get("/categories/<int:category_id>/items/<int:item_id>")
@get_item
def get_item_by_id(item, **_):
    return ItemSchema().jsonify(item)


@app.put("/categories/<int:category_id>/items/<int:item_id>")
@require_token
@use_request_schema(ItemUpdateSchema)
@get_item
def update_item(item, user, request_data, **_):
    if item.user_id != user.id:
        raise Forbidden()

    if request_data.get("name"):
        item_with_same_name = ItemModel.query_by_name(request_data["name"])
        if item_with_same_name and item_with_same_name.id != item.id:
            raise DuplicatedItemNameError()

        item.name = request_data["name"]

    if request_data.get("description"):
        item.description = request_data["description"]

    db.session.commit()

    return {}


@app.delete("/categories/<int:category_id>/items/<int:item_id>")
@require_token
@get_item
def delete_item(item, user, **_):
    if item.user_id != user.id:
        raise Forbidden()

    db.session.delete(item)
    db.session.commit()

    return {}
