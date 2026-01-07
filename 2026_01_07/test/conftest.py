import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_collection

@pytest.fixture(scope='session')
def client():
    return TestClient(app)

@pytest.fixture(scope='function')
def embedding_collection():
    collection = get_collection("embeddings")
    existing = {
        doc["_id"] for doc in collection.find({}, {"_id":1})
    }
    yield collection

    for doc in collection.find({}, {"_id":1}):
        if doc["_id"] not in existing:
            collection.delete_one({"id":doc["_id"]})