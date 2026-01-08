from ..database import get_collection
from bson import ObjectId
from typing import List, Dict

COLLECTION_NAME = 'embeddings'
CHUNK_COLLECTION_NAME = 'chunk_embeddings'

collection = get_collection(COLLECTION_NAME)
chunk_collection = get_collection(CHUNK_COLLECTION_NAME)

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

def save_chunk_embeddings(chunks: List[str], embeddings: List[List[float]]) -> List[str]:
    docs = []
    for chunk, embedding in zip(chunks, embeddings):
        doc = {
            "text": chunk,
            "embedding": embedding
        }
        docs.append(doc)
    
    result = chunk_collection.insert_many(docs)
    return [str(id) for id in result.inserted_ids]

def search_similar_chunks(query_embedding: List[float], top_k: int = 3) -> List[Dict]:
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": top_k
            }
        },
        {
            "$project": {
                "text": 1,
                "score": {"$meta": "vectorSearchScore"},
                "_id": 0
            }
        }
    ]
    
    results = list(chunk_collection.aggregate(pipeline))
    return results