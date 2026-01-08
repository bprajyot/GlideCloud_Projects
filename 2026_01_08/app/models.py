from pydantic import BaseModel
from typing import List

class EmbedRequest(BaseModel):
    text: str

class EmbedResponse(BaseModel):
    text: str
    embedding: List[float]
    id: str=None

class SearchRequest(BaseModel):
    query: str

class ChunkResponse(BaseModel):
    text: str
    score: float