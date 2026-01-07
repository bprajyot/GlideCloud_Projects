from ..database import get_collection
from bson import ObjectId

COLLECTION_NAME = 'embeddings'
collection = get_collection(COLLECTION_NAME)

def save_embedding(text, embedding)->str:
    doc = {
        "text": text,
        "embedding":embedding
    }
    result = collection.insert_one(doc)
    return str(result.inserted_id)

def get_embedding_by_id(id):
    doc = collection.find_one({"_id":ObjectId(id)})
    if doc:
        return {
            "id": str(doc["_id"]),
            "text": doc["text"],
            "embedding": doc["embedding"]
        }
    return None