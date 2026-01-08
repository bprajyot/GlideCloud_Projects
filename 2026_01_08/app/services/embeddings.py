import ollama
from ..config import OLLAMA_MODEL


def get_embedding(text)-> list:
    response = ollama.embed(model=OLLAMA_MODEL, input=text)
    return response['embeddings'][0]