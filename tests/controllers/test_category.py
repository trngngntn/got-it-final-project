from main import config
from main.commons.exceptions import BadRequest, Forbidden, NotFound, Unauthorized
from main.libs.jwt import verify_access_token
from main.models.category import CategoryModel
from main.models.item import ItemModel


# GET /categories
# 200
def test_get_all_categories(client, categories):
    response = client.get("/categories")
    assert response.status_code == 200

    category_list = response.json["data"]

    assert len(category_list) <= config.PAGINATION_MAX_ITEMS
    assert response.json["items_per_page"] == config.PAGINATION_MAX_ITEMS

    total_category = len(categories)
    assert response.json["total_items"] == total_category

    # test with page > 1
    page = 1

    while page * config.PAGINATION_MAX_ITEMS < total_category:
        page = page + 1
        response = client.get(f"/categories?page={page}")
        assert response.status_code == 200
        assert type(response.json["data"][0]["name"]) is str

    # test with page > max_page
    response = client.get(f"/categories?page={page + 1}")

    assert response.status_code == 404
    assert response.json == NotFound().to_dict()


# POST /categories
# 201
def test_create_category(client, login_users):
    response = client.post(
        "/categories",
        headers={"Authorization": f"Bearer {login_users[0]}"},
        json={"name": "categoryx"},
    )

    assert response.status_code == 201
    assert response.json == {}

    created = CategoryModel.query.filter(CategoryModel.name == "categoryx").first()

    assert created is not None
    assert created.user_id == verify_access_token(login_users[0])["sub"]


# 400/000
def test_create_category_with_malformed_request(
    client,
    login_users,
):
    response = client.post(
        "/categories",
        headers={"Authorization": f"Bearer {login_users[0]}"},
        data="{name: abcd}",
    )

    assert response.status_code == 400
    assert response.json == BadRequest().to_dict()


# 400/001
def test_create_category_with_long_name(
    client,
    login_users,
):
    response = client.post(
        "/categories",
        headers={"Authorization": f"Bearer {login_users[0]}"},
        json={"name": "123456789012345678901234567890123456789012345678901234567890"},
    )

    assert response.status_code == 400
    assert response.json["error_code"] == 400001


# 401
def test_create_category_without_auth(client):
    response = client.post(
        "/categories",
        headers={"Authorization": "abcd"},
        json={"name": "category"},
    )

    assert response.status_code == 401
    assert response.json == Unauthorized().to_dict()


# 409
# use pytest parameterize
def test_create_category_with_duplicated_name(client, login_users):
    test_create_category(client, login_users)

    response = client.post(
        "/categories",
        headers={"Authorization": f"Bearer {login_users[0]}"},
        json={"name": "categoryx"},
    )

    assert response.status_code == 409
    assert response.json["error_code"] == 409002


# GET /categories/{id}
# 200
def test_get_category(categories, client):
    response = client.get(f"/categories/{categories[0].id}")

    assert response.status_code == 200

    data = response.json

    assert type(data["id"]) is int
    assert type(data["user_id"]) is int
    assert type(data["name"]) is str


# 404
def test_get_category_with_invalid_id(client, categories):
    response = client.get("/categories/99999")

    assert response.status_code == 404
    assert response.json == NotFound().to_dict()


# PUT /categories/{id}
# 200
def test_update_category(client, login_users, categories):
    user = categories[0].user_id
    for i in range(0, len(login_users)):
        if verify_access_token(login_users[i])["sub"] == user:
            user = login_users[i]
            break

    response = client.put(
        f"/categories/{categories[0].id}",
        headers={"Authorization": f"Bearer {user}"},
        json={"name": "new name"},
    )

    assert response.status_code == 200
    assert response.json == {}

    updated = CategoryModel.query.filter(CategoryModel.name == "new name").first()

    assert updated
    assert updated.id == categories[0].id


# 400
def test_update_category_with_malformed_request(client, login_users, categories):
    user = categories[0].user_id
    for i in range(0, len(login_users)):
        if verify_access_token(login_users[i])["sub"] == user:
            user = login_users[i]
            break

    response = client.put(
        f"/categories/{categories[0].id}",
        headers={"Authorization": f"Bearer {user}"},
        data="{{}",
    )

    assert response.status_code == 400
    assert response.json == BadRequest().to_dict()


# 401
def test_update_category_without_auth(client, categories):
    response = client.put(
        f"/categories/{categories[0].id}",
        json={"name": "new name"},
    )

    assert response.status_code == 401
    assert response.json == Unauthorized().to_dict()


# 403
def test_update_category_of_other_user(client, login_users, categories):
    user = login_users[0]
    if categories[0].user_id == verify_access_token(login_users[0])["sub"]:
        user = login_users[1]
    response = client.put(
        f"/categories/{categories[0].id}",
        headers={"Authorization": f"Bearer {user}"},
        json={"name": "new name"},
    )

    assert response.status_code == 403
    assert response.json == Forbidden().to_dict()


# 404
def test_update_category_with_invalid_id(
    client,
    login_users,
    categories,
):
    response = client.put(
        "/categories/99999",
        headers={"Authorization": f"Bearer {login_users[0]}"},
        json={"name": "new name"},
    )

    assert response.status_code == 404
    assert response.json == NotFound().to_dict()


# 409
def test_update_category_with_duplicated_name(
    client,
    login_users,
    categories,
):
    test_update_category(client, login_users, categories)
    user = categories[1].user_id
    for i in range(0, len(login_users)):
        if verify_access_token(login_users[i])["sub"] == user:
            user = login_users[i]
            break

    response = client.put(
        f"/categories/{categories[1].id}",
        headers={"Authorization": f"Bearer {user}"},
        json={"name": "new name"},
    )

    assert response.status_code == 409
    assert response.json["error_code"] == 409002


# DELETE /categories/{id}
# 200
def test_delete_category(client, login_users, categories, items):
    user = categories[0].user_id
    for i in range(0, len(login_users)):
        if verify_access_token(login_users[i])["sub"] == user:
            user = login_users[i]
            break
    response = client.delete(
        f"/categories/{categories[0].id}",
        headers={"Authorization": f"Bearer {user}"},
    )

    assert response.status_code == 200
    assert response.json == {}
    assert (
        ItemModel.query.filter(ItemModel.category_id == categories[0].id).first()
        is None
    )


# 401
def test_delete_category_without_auth(client, categories):
    response = client.delete(
        f"/categories/{categories[0].id}",
        data="{{}",
    )

    assert response.status_code == 401
    assert response.json == Unauthorized().to_dict()


# 403
def test_delete_category_of_other_user(client, login_users, categories):
    user = login_users[0]
    if categories[0].user_id == verify_access_token(login_users[0])["sub"]:
        user = login_users[1]

    response = client.delete(
        f"/categories/{categories[0].id}",
        headers={"Authorization": f"Bearer {user}"},
    )

    assert response.status_code == 403
    assert response.json == Forbidden().to_dict()


# 404
def test_delete_category_with_invalid_id(
    client,
    login_users,
    categories,
):
    response = client.delete(
        "/categories/99999",
        headers={"Authorization": f"Bearer {login_users[0]}"},
    )

    assert response.status_code == 404
    assert response.json == NotFound().to_dict()
