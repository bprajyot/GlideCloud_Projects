from fastapi import APIRouter, HTTPException, UploadFile, File
from ..models import EmbedRequest, EmbedResponse, SearchRequest, ChunkResponse
from ..services.embeddings import get_embedding
from ..services.db import save_embedding, get_embedding_by_id, save_chunk_embeddings, search_similar_chunks
from ..services.pdf import extract_text_from_pdf, chunk_text
from typing import List

router = APIRouter(prefix="/embeddings")

@router.post("/", response_model=EmbedResponse)
def create_embedding(request: EmbedRequest):
    embedding = get_embedding(request.text)
    doc_id = save_embedding(request.text, embedding)
    return EmbedResponse(text=request.text, embedding=embedding, id=doc_id)

@router.get("/{doc_id}", response_model=EmbedResponse)
def read_embedding(doc_id: str):
    result = get_embedding_by_id(doc_id)
    if not result:
        raise HTTPException(status_code=404, detail="Embedding not found")
    return EmbedResponse(**result)

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        pdf_bytes = await file.read()
        
        text = extract_text_from_pdf(pdf_bytes)
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in PDF")
        
        chunks = chunk_text(text)
        embeddings = [get_embedding(chunk) for chunk in chunks]
        doc_ids = save_chunk_embeddings(chunks, embeddings)
        
        return {
            "message": "PDF processed successfully",
            "filename": file.filename,
            "chunks_created": len(chunks),
            "document_ids": doc_ids
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@router.post("/search", response_model=List[ChunkResponse])
def search_chunks(request: SearchRequest):
    try:
        query_embedding = get_embedding(request.query)
        results = search_similar_chunks(query_embedding, 3)
        return [ChunkResponse(text=r["text"], score=r["score"]) for r in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching chunks: {str(e)}")
