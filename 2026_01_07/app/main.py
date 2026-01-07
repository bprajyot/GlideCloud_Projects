from fastapi import FastAPI
from .routes import routes

app = FastAPI(
    title="FastAPI + Ollama Embeddings API",
    description="API to generate embeddings using Ollama and store them in MongoDB Atlas",
    version="1.0.0"
)

# Include routers
app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI + Ollama + MongoDB Embeddings API"}
