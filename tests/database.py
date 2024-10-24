from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app import database
from fastapi.testclient import TestClient
from app.main import app
import pytest

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
@pytest.fixture(scope="module")
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

@pytest.fixture(scope="module")
def client(setup_db):
    return TestClient(app)



