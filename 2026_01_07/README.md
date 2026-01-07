# Embeddings API (FastAPI + Ollama + MongoDB)

A simple system to generate text embeddings using **Ollama**, store them in **MongoDB**, and retrieve them via REST APIs.

---

## Features

- Generate embedding from input text  
- Store embeddings in MongoDB  
- Retrieve embedding by document ID  
- Auto-generated API documentation  

---

## Tech Stack

- **Backend**: FastAPI  
- **Embedding Engine**: Ollama  
- **Database**: MongoDB (Atlas)  
- **Language**: Python  
- **API Docs**: Swagger (OpenAPI)  

---

## How to Run

- Start MongoDB and ensure it is running  
- Start Ollama locally  
- Create a `.env` file with required environment variables  
- Install dependencies:
  ```bash
  pip install -r requirements.txt


## API Testing
Testing can be done using the usual url: http://127.0.0.1:8000/docs