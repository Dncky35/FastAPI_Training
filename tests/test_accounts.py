from fastapi import status
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.testclient import TestClient
from app.main import app
from app import schemas, config, database

SQLALCHEMY_DATABASE_URL = f'postgresql://fastapi_user:784512@localhost:5432/fastapi_training_testing'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Testing_SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
# database.Base.metadata.create_all(bind=engine)

def override_get_db():
    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[database.get_db] = override_get_db

# Pytest fixture to manage database setup/teardown
@pytest.fixture(scope="function")
def setup_db():
    # Create tables
    database.Base.metadata.create_all(bind=engine)

    # Begin a transaction
    connection = engine.connect()
    transaction = connection.begin()

    # Use the same connection for the session
    Testing_SessionLocal.configure(bind=connection)
    
    yield connection

    # Rollback the transaction after each test
    transaction.rollback()
    connection.close()

    # Drop tables if needed (optional, since transactions are rolled back)
    # Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(setup_db):
    return TestClient(app)

def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "welcome to main page"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("test@testmail.com", "123456789Password", 201)
])
def test_create_user(client, email, password, status_code):
    res = client.post("/accounts/", json={
        "email":email,
        "password":password
    })

    test_account = schemas.Account(**res.json())
    assert test_account.email == email
    assert res.status_code == status_code
