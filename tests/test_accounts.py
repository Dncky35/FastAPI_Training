import pytest
from app import schemas, config
from jose import jwt

def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "welcome to main page"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("test@testmail.com", "123456789Password", 201)
])

def test_create_account(client, email, password, status_code):
    res = client.post("/accounts/", json={
        "email":email,
        "password":password
    })

    test_account = schemas.Account(**res.json())
    assert test_account.email == email
    assert res.status_code == status_code

def test_login_account(client, test_account):
    res = client.post("/login/", data={"username":test_account["email"], "password":test_account["password"]})
    # print(res.json())

    test_token = schemas.Token(**res.json())

    payload = jwt.decode(test_token.access_token, config.settings.secret_key, algorithms=[config.settings.algorithm])
    id:str = payload.get("account_id")

    assert id == test_account["id"]
    assert test_token.token_type == "Bearer"
    assert res.status_code == 202

@pytest.mark.parametrize("email, password, status_code", [
    ("test@testmail.com", "784512", 403),
    ("test@qwers.com", "123456789Password", 403),
    ("test@qwers.com", "784512", 403),
    ("test@qwers.com", None, 422),
    (None, "784512", 422)
])

def test_incorrect_login(client, test_account, email, password, status_code):
    res = client.post("/login/", data={"username":email, "password": password})
    
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"