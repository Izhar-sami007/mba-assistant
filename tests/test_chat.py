import pytest
from src.config import settings
from src.rag_chain import build_vectorstore, make_chain
from langchain_core.documents import Document

@pytest.mark.skipif(settings.llm_provider=="openai" and not settings.openai_api_key, reason="needs OpenAI key or use Ollama")
def test_chat_simple():
    docs = [Document(page_content="Demand-pull inflation is caused by increased demand.", metadata={"source":"eco.pdf"})]
    vs = build_vectorstore(docs, settings.persist_dir)
    chain = make_chain(vs)
    out = chain.invoke("What is demand-pull inflation?")
    assert isinstance(out, str) and len(out) > 0
