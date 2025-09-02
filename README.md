# MBA Student Assistant Chatbot

A retrieval‑augmented chatbot tailored for MBA students. Ingest course PDFs, notes, previous year papers, teacher/subject CSVs, etc. Query them via a FastAPI API and optional Streamlit UI.

## Features
- PDF/DOCX/CSV loaders
- FAISS vector store
- **Ollama (local llama3)** by default; OpenAI optional
- FastAPI REST endpoints
- Streamlit front‑end
- Simple tests & CI

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip && pip install -r requirements.txt
cp .env.example .env   # defaults to ollama (local)
# Put your PDFs/CSVs/DOCX into data/raw/
python -m src.ingest --input_dir data/raw --persist_dir data/vectorstore
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
# optional UI
streamlit run src/ui_streamlit.py
```

## API
- `POST /ingest` — rebuild vector store from `data/raw`
- `POST /chat` — body: `{ "query": "..." }`

## Docker
```bash
docker compose up --build
```

## Notes
- Keep documents in `data/raw/`; FAISS index in `data/vectorstore/`.
