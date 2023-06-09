from main.commons.exceptions import BadRequest, Unauthorized
from main.libs.jwt import verify_access_token


# POST /register
# 201
def test_user_register(client):
    response = client.post(
        "/register", json={"email": "abc@gmail.com", "password": "123Abc"}
    )
    assert response.status_code == 201
    assert verify_access_token(response.json["access_token"])


# 400/000
def test_user_register_with_malformed_req(client):
    response = client.post("/register", data="{{}")
    assert response.status_code == 400
    assert response.json == BadRequest().to_dict()


# 400/001
def test_user_resister_with_invalid_credentials(client):
    response = client.post(
        "/register", json={"email": "not_email", "password": "Ws2ok3"}
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001

    response = client.post(
        "/register", json={"email": "not_email@abc.com", "password": "11aabb"}
    )
    assert response.status_code == 400
    assert response.json["error_code"] == 400001


# 409
def test_user_register_with_duplicated_email(client):
    test_user_register(client)
    response = client.post(
        "/register", json={"email": "abc@gmail.com", "password": "111Axs"}
    )
    assert response.status_code == 409
    assert response.json["error_code"] == 409001


# POST /login
# 200
def test_user_login(client):
    test_user_register(client)
    response = client.post(
        "/login", json={"email": "abc@gmail.com", "password": "123Abc"}
    )
    assert response.status_code == 200
    assert verify_access_token(response.json["access_token"])


# 400
def test_user_login_with_malformed_req(client):
    response = client.post("/login", data="{{}")
    assert response.status_code == 400
    assert response.json == BadRequest().to_dict()


# 401
def test_user_login_with_wrong_credentials(client):
    response = client.post(
        "/login", json={"email": "abc@gmail.com", "password": "Abc134"}
    )
    assert response.status_code == 401
    assert response.json == Unauthorized().to_dict()
