# tests/test_user.py
def test_user_creates_embedding(client, embedding_collection):
    text = {
        "text": "Hello from pytest user test"
    }

    response = client.post("/embeddings/", json=text)

    assert response.status_code == 200

    data = response.json()
    assert data["text"] == text["text"]
    assert isinstance(data["embedding"], list)
    assert len(data["embedding"]) > 0
    assert isinstance(data["id"], str)

    # Verify document exists in DB
    doc = embedding_collection.find_one({"text": text["text"]})
    assert doc is not None


def test_user_reads_embedding(client):
    """
    User retrieves an embedding by ID
    """
    # Create embedding first
    create_response = client.post(
        "/embeddings/",
        json={"text": "Read test"}
    )

    doc_id = create_response.json()["id"]

    # Fetch it
    response = client.get(f"/embeddings/{doc_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == doc_id
    assert data["text"] == "Read test"
    assert isinstance(data["embedding"], list)


def test_user_requests_nonexistent_embedding(client):
    """
    User requests an embedding that does not exist
    """
    fake_id = "64b000000000000000000000"

    response = client.get(f"/embeddings/{fake_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Embedding not found"
