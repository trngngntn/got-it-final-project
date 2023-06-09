from main import config
from main.commons.exceptions import BadRequest, Forbidden, NotFound, Unauthorized
from main.libs.jwt import verify_access_token
from main.models.item import ItemModel


# GET /categories/{cat_id}/items
# 200
def test_get_all_items(client, categories, items):
    path = f"/categories/{categories[0].id}/items"
    response = client.get(path)
    assert response.status_code == 200

    catergory_list = response.json["data"]

    assert len(catergory_list) <= config.PAGINATION_MAX_ITEMS
    assert response.json["items_per_page"] == config.PAGINATION_MAX_ITEMS

    total_item = response.json["total_items"]

    # test with page > 1
    page = 1

    while page * config.PAGINATION_MAX_ITEMS < total_item:
        page = page + 1
        response = client.get(f"{path}?page={page}")
        assert response.status_code == 200
        data = response.json["data"][0]
        assert type(data["name"]) is str
        assert type(data["description"]) is str

    # test with page > max_page
    response = client.get(f"{path}?page={page + 1}")

    assert response.status_code == 404
    assert response.json == NotFound().to_dict()


# POST /categories/{cat_id}/items
# 201
def test_create_item(client, login_users, categories):
    response = client.post(
        f"/categories/{categories[0].id}/items",
        headers={"Authorization": f"Bearer {login_users[0]}"},
        json={"name": "itemx", "description": "an item"},
    )

    assert response.status_code == 201
    assert response.json == {}

    created = ItemModel.query.filter(ItemModel.name == "itemx").first()

    assert created
    assert created.user_id == verify_access_token(login_users[0])["sub"]
    assert created.category_id == categories[0].id


# 400
def test_create_item_with_malformed_request(
    client,
    login_users,
    categories,
):
    response = client.post(
        f"/categories/{categories[0].id}/items",
        headers={"Authorization": f"Bearer {login_users[0]}"},
        data="{name: abcd}",
    )

    assert response.status_code == 400
    assert response.json == BadRequest().to_dict()


# 401
def test_create_item_without_auth(client, categories):
    response = client.post(
        f"/categories/{categories[0].id}/items",
        json={"name": "item", "description": "an item"},
    )

    assert response.status_code == 401
    assert response.json == Unauthorized().to_dict()


# 404
def test_create_item_with_invalid_category_id(
    client,
    login_users,
    categories,
):
    response = client.post(
        "/categories/99999/items",
        headers={"Authorization": f"Bearer {login_users[0]}"},
        json={"name": "item", "description": "an item"},
    )

    assert response.status_code == 404
    assert response.json == NotFound().to_dict()


# 409
def test_create_item_with_duplicated_name(client, login_users, categories):
    test_create_item(client, login_users, categories)

    response = client.post(
        f"/categories/{categories[0].id}/items",
        headers={"Authorization": f"Bearer {login_users[0]}"},
        json={"name": "itemx", "description": "an item"},
    )

    assert response.status_code == 409
    assert response.json["error_code"] == 409003


# GET /categories/{cat_id}/items/{itm_id}
# 200
def test_get_item(items, client):
    response = client.get(f"/categories/{items[0].category_id}/items/{items[0].id}")

    assert response.status_code == 200

    data = response.json

    assert type(data["id"]) is int
    assert type(data["user_id"]) is int
    assert type(data["category_id"]) is int
    assert type(data["name"]) is str
    assert type(data["description"]) is str


# 404
def test_get_item_with_invalid_ids(client, categories, items):
    response = client.get(f"/categories/{categories[0].id}/items/99999")

    assert response.status_code == 404
    assert response.json == NotFound().to_dict()

    response = client.get(f"/categories/99999/items/{items[0].id}")

    assert response.status_code == 404
    assert response.json == NotFound().to_dict()


# PUT /categories/{cat_id}/items/{itm_id}
# 200
def test_update_item(client, login_users, items):
    user = items[0].user_id

    for i in range(0, len(login_users)):
        if verify_access_token(login_users[i])["sub"] == user:
            user = login_users[i]
            break

    response = client.put(
        f"/categories/{items[0].category_id}/items/{items[0].id}",
        headers={"Authorization": f"Bearer {user}"},
        json={"description": "new description"},
    )

    assert response.status_code == 200
    assert response.json == {}

    response = client.put(
        f"/categories/{items[0].category_id}/items/{items[0].id}",
        headers={"Authorization": f"Bearer {user}"},
        json={"name": "new name"},
    )

    assert response.status_code == 200
    assert response.json == {}

    updated = ItemModel.query.filter(ItemModel.name == "new name").first()

    assert updated
    assert updated.id == items[0].id
    assert updated.description == "new description"


# 400/000
def test_update_item_with_malformed_request(client, login_users, items):
    user = items[0].user_id

    for i in range(0, len(login_users)):
        if verify_access_token(login_users[i])["sub"] == user:
            user = login_users[i]
            break

    response = client.put(
        f"/categories/{items[0].category_id}/items/{items[0].id}",
        headers={"Authorization": f"Bearer {user}"},
        data="{{}",
    )

    assert response.status_code == 400
    assert response.json == BadRequest().to_dict()


# 401
def test_update_item_without_auth(client, items):
    response = client.put(
        f"/categories/{items[0].category_id}/items/{items[0].id}",
        json={"name": "new name", "description": "new description"},
    )

    assert response.status_code == 401
    assert response.json == Unauthorized().to_dict()


# 403
def test_update_item_of_other_user(client, login_users, items):
    user = login_users[0]
    if items[0].user_id == verify_access_token(login_users[0])["sub"]:
        user = login_users[1]

    response = client.put(
        f"/categories/{items[0].category_id}/items/{items[0].id}",
        headers={"Authorization": f"Bearer {user}"},
        json={"name": "new name"},
    )

    assert response.status_code == 403
    assert response.json == Forbidden().to_dict()


# 404
def test_update_item_with_invalid_id(
    client,
    login_users,
    categories,
    items,
):
    response = client.put(
        f"/categories/99999/items/{items[0].id}",
        headers={"Authorization": f"Bearer {login_users[0]}"},
        json={"name": "new name"},
    )

    assert response.status_code == 404
    assert response.json == NotFound().to_dict()

    response = client.put(
        f"/categories/{categories[0].id}/items/99999",
        headers={"Authorization": f"Bearer {login_users[0]}"},
        json={"name": "new name"},
    )

    assert response.status_code == 404
    assert response.json == NotFound().to_dict()


# 409
def test_update_item_with_duplicated_name(client, login_users, items):
    test_update_item(client, login_users, items)
    user = items[1].user_id

    for i in range(0, len(login_users)):
        if verify_access_token(login_users[i])["sub"] == user:
            user = login_users[i]
            break

    response = client.put(
        f"/categories/{items[1].category_id}/items/{items[1].id}",
        headers={"Authorization": f"Bearer {user}"},
        json={"name": "new name"},
    )

    assert response.status_code == 409
    assert response.json["error_code"] == 409003


# DELETE /categories/{cat_id}/items/{itm_id}
# 200
def test_delete_item(client, login_users, items):
    user = items[0].user_id

    for i in range(0, len(login_users)):
        if verify_access_token(login_users[i])["sub"] == user:
            user = login_users[i]
            break

    response = client.delete(
        f"/categories/{items[0].category_id}/items/{items[0].id}",
        headers={"Authorization": f"Bearer {user}"},
    )

    assert response.status_code == 200
    assert response.json == {}

    assert ItemModel.query.filter(ItemModel.category_id == items[0].id).first() is None


# 401
def test_delete_item_without_auth(client, items):
    response = client.delete(
        f"/categories/{items[0].category_id}/items/{items[0].id}",
        data="{{}",
    )

    assert response.status_code == 401
    assert response.json == Unauthorized().to_dict()


# 403
def test_delete_item_of_other_user(client, login_users, items):
    user = login_users[0]

    if items[0].user_id == verify_access_token(login_users[0])["sub"]:
        user = login_users[1]

    response = client.delete(
        f"/categories/{items[0].category_id}/items/{items[0].id}",
        headers={"Authorization": f"Bearer {user}"},
    )

    assert response.status_code == 403
    assert response.json == Forbidden().to_dict()


# 404
def test_delete_item_with_invalid_id(
    client,
    login_users,
    categories,
    items,
):
    response = client.delete(
        f"/categories/99999/items/{items[0].id}",
        headers={"Authorization": f"Bearer {login_users[0]}"},
    )

    assert response.status_code == 404
    assert response.json == NotFound().to_dict()

    response = client.delete(
        f"/categories/{categories[0].id}/items/99999",
        headers={"Authorization": f"Bearer {login_users[0]}"},
    )

    assert response.status_code == 404
    assert response.json == NotFound().to_dict()
