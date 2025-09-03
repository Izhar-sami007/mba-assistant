import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="MBA Student Assistant", page_icon="🎓")
st.title("🎓 MBA Student Assistant")

with st.sidebar:
    st.header("Actions")
    if st.button("(Re)Ingest Documents"):
        r = requests.post(f"{API_URL}/ingest")
        st.success(r.json())

user_q = st.text_input("Ask a question from your MBA materials:", placeholder="e.g., Explain demand-pull vs cost-push inflation")
if st.button("Ask") and user_q:
    with st.spinner("Thinking..."):
        r = requests.post(f"{API_URL}/chat", json={"query": user_q})
        if r.ok:
            st.markdown(r.json()["answer"])
        else:
            st.error(r.text)
