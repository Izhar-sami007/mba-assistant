from __future__ import annotations
import argparse
import glob
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from .rag_chain import build_vectorstore, save_vectorstore
from .config import settings
from .utils import logger, timer

LOADERS = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".csv": CSVLoader,
}

def load_documents(input_dir: str) -> list[Document]:
    paths = []
    for ext in LOADERS:
        paths.extend(glob.glob(str(Path(input_dir) / f"**/*{ext}"), recursive=True))
    if not paths:
        logger.warning("No documents found in %s", input_dir)
    docs: list[Document] = []
    for p in paths:
        ext = Path(p).suffix.lower()
        loader_cls = LOADERS[ext]
        if ext == ".csv":
            loader = loader_cls(file_path=p, encoding="utf-8")
        else:
            loader = loader_cls(p)
        loaded = loader.load()
        for d in loaded:
            d.metadata = {**d.metadata, "source": str(Path(p).name)}
        docs.extend(loaded)
    return docs

def chunk_documents(docs: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        add_start_index=True,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(docs)

def main(input_dir: str, persist_dir: str):
    Path(persist_dir).mkdir(parents=True, exist_ok=True)
    with timer("Ingestion"):
        docs = load_documents(input_dir)
        chunks = chunk_documents(docs)
        vs = build_vectorstore(chunks, persist_dir)
        save_vectorstore(vs, persist_dir)
        logger.info("Indexed %d chunks from %d files", len(chunks), len(set(d.metadata['source'] for d in chunks)))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input_dir", default="data/raw")
    ap.add_argument("--persist_dir", default=settings.persist_dir)
    args = ap.parse_args()
    main(args.input_dir, args.persist_dir)
