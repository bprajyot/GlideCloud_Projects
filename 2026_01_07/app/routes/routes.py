from fastapi import APIRouter, HTTPException
from ..models import EmbedRequest, EmbedResponse
from ..services.embeddings import get_embedding
from ..services.db import save_embedding, get_embedding_by_id

router = APIRouter(prefix="/embeddings", tags=["Embeddings"])

@router.post("/", response_model=EmbedResponse)
def create_embedding(request: EmbedRequest):
    """
    Create an embedding from input text and store it in MongoDB.
    """
    embedding = get_embedding(request.text)
    doc_id = save_embedding(request.text, embedding)
    return EmbedResponse(text=request.text, embedding=embedding, id=doc_id)

@router.get("/{doc_id}", response_model=EmbedResponse)
def read_embedding(doc_id: str):
    """
    Retrieve an embedding by document ID.
    """
    result = get_embedding_by_id(doc_id)
    if not result:
        raise HTTPException(status_code=404, detail="Embedding not found")
    return EmbedResponse(**result)
