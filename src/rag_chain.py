from __future__ import annotations
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from .config import settings

SYSTEM_PROMPT = (
    "You are an MBA Student Assistant. Answer with clear, concise explanations,"
    " practical examples, and cite the given sources as [Doc i] where i is the chunk index."
    " If unsure, say so and suggest how to find the answer in the provided materials."
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "Question: {question}\n\nContext:{context}\n\nAnswer:")
])

def load_embeddings():
    return HuggingFaceEmbeddings(model_name=settings.embeddings_model)

def build_vectorstore(docs: List[Document], persist_dir: str) -> FAISS:
    embed = load_embeddings()
    return FAISS.from_documents(docs, embed)

def load_vectorstore(persist_dir: str) -> FAISS:
    embed = load_embeddings()
    return FAISS.load_local(persist_dir, embed, allow_dangerous_deserialization=True)

def save_vectorstore(vs: FAISS, persist_dir: str):
    vs.save_local(persist_dir)

def get_llm():
    if settings.llm_provider == "ollama":
        return Ollama(model=settings.ollama_model)
    return ChatOpenAI(model=settings.openai_model, temperature=0)  # requires OPENAI_API_KEY

def make_chain(vs: FAISS):
    retriever = vs.as_retriever(search_kwargs={"k": settings.top_k})

    def format_docs(docs: List[Document]):
        parts = []
        for i, d in enumerate(docs, 1):
            meta = d.metadata
            src = meta.get("source", "doc")
            parts.append(f"\n[Doc {i}] ({src})\n{d.page_content}")
        return "\n".join(parts)

    llm = get_llm()

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
