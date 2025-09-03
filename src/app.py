from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel
from .config import settings
from .rag_chain import load_vectorstore, make_chain
from .ingest import main as ingest_main

app = FastAPI(title="MBA Student Assistant API", version="1.0.0")

class ChatRequest(BaseModel):
    query: str

@app.post("/ingest")
def ingest():
    ingest_main("data/raw", settings.persist_dir)
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    vs = load_vectorstore(settings.persist_dir)
    chain = make_chain(vs)
    answer = chain.invoke(req.query)
    return {"answer": answer}

@app.get("/")
def root():
    return {"message": "MBA Student Assistant is running", "docs": "/docs"}
