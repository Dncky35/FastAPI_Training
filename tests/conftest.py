from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app import database, oauth2, schemas, models
from app.config import settings
from fastapi.testclient import TestClient
from app.main import app
import pytest
import uuid

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_testing'
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

@pytest.fixture()
def session():
    print("my session fixture ran")
    database.Base.metadata.drop_all(bind=engine)
    database.Base.metadata.create_all(bind=engine)
    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[database.get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_account(client):
    user_data = {
        "email":f"user_{uuid.uuid4()}@example.com",  # Generates a unique email,
        "password":"123456789Password"
    }
    res = client.post("/accounts", json=user_data)

    assert res.status_code == 201
    test_account = res.json()
    test_account['password'] = user_data["password"]

    return test_account


@pytest.fixture
def test_account_2(client):
    user_data = {
        "email":f"user_{uuid.uuid4()}@example.com",  # Generates a unique email,
        "password":"123456789Password"
    }
    res = client.post("/accounts", json=user_data)

    assert res.status_code == 201
    test_account = res.json()
    test_account['password'] = user_data["password"]

    return test_account

@pytest.fixture
# access_token = oauth2.create_access_token(data = {"account_id":account.id})
def token_test(test_account):
    token = oauth2.create_access_token(data = {"account_id":test_account['id']})
    return token

@pytest.fixture
def authorized_client(client, token_test):
    
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_test}"
    }

    return client

@pytest.fixture
def test_posts(test_account, test_account_2, session):
    
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "account_id": test_account['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "account_id": test_account['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "account_id": test_account['id']
    }, {
        "title": "4rd title",
        "content": "4rd content",
        "account_id": test_account_2['id']
    }]

    def create_post_list(post):
        return models.Post(**post)

    posts_map = map(create_post_list, posts_data)
    posts = list(posts_map)
    session.add_all(posts)

    # for element in posts_data:
    #     session.add(models.Post(title=element.title, content=element.content, account_id=element.test_account['id']))

    session.commit()

    posts = session.query(models.Post).all()
    return posts