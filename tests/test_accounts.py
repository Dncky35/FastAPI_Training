import pytest
from app.main import app
from app import schemas
from .database import client, setup_db

def test_root(setup_db, client):
    res = client.get("/")
    assert res.json().get("message") == "welcome to main page"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("test@testmail.com", "123456789Password", 201)
])

def test_create_user(setup_db, client, email, password, status_code):
    res = client.post("/accounts/", json={
        "email":email,
        "password":password
    })

    test_account = schemas.Account(**res.json())
    assert test_account.email == email
    assert res.status_code == status_code
