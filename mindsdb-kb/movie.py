import streamlit as st
import os

import requests
import json
import pandas as pd
from datetime import datetime

# Constants
OLLAMA_MODEL = "llama2"
OLLAMA_HOST = "http://localhost:11434"
CACHE_FILE = "qa_cache.jsonl"

# Dummy KB search
def search_kb(query: str, limit: int = 100) -> pd.DataFrame:
    return pd.DataFrame({
        'id': [1],
        'chunk_content': [
            "In 'Home Alone', a boy defends his home against two burglars named Harry and Marv on Christmas Eve."
        ],
        'relevance': [0.99]
    })

def clean_output(text: str) -> str:
    cleaned = text.replace('\n', ' ').strip()
    while '  ' in cleaned:
        cleaned = cleaned.replace('  ', ' ')
    return cleaned

def read_streamed_response(response):
    full_answer = ""
    for line in response.iter_lines():
        if line:
            try:
                obj = json.loads(line.decode('utf-8'))
                full_answer += obj.get("message", {}).get("content", "")
            except:
                continue
    return clean_output(full_answer)

def save_to_cache(question, answer, used_chunks):
    record = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "used_chunks": used_chunks
    }
    with open(CACHE_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record) + '\n')

def get_llm_answer(question: str, context_chunks: list) -> str:
    context = "\n---\n".join(context_chunks)

    prompt = f"""You are a movie expert assistant. Based *only* on the following movie summaries (context),
answer the user's question. If the context doesn't contain the answer,
state that you cannot answer based on the provided information.
Return only the plain answer as a single paragraph, with no JSON or markdown formatting.

CONTEXT:
{context}

QUESTION:
{question}
"""
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that answers questions about movies using only the provided context."},
                    {"role": "user", "content": prompt}
                ],
                "stream": True,
                "temperature": 0.0
            },
            stream=True
        )
        response.raise_for_status()
        return read_streamed_response(response)
    except Exception as e:
        return f"⚠️ Error with Ollama: {e}"

# -------------- Streamlit UI ------------------
st.set_page_config(page_title="Movie KB QA", layout="centered")
st.title("🎬 Movie Knowledge Base Q&A")

question = st.text_input("Ask a movie-related question:")
if st.button("Get Answer") and question.strip() != "":
    with st.spinner("Searching knowledge base..."):
        chunks_df = search_kb(question)
        used_chunks = chunks_df['chunk_content'].tolist()
        st.subheader("🔍 Top Relevant Chunks:")
        for i, row in chunks_df.iterrows():
            st.markdown(f"**Chunk {i+1} (Score: {row['relevance']}):**\n> {row['chunk_content']}")

    with st.spinner("Calling Ollama model..."):
        answer = get_llm_answer(question, used_chunks)

    st.success("✅ Answer generated!")
    st.markdown(f"**Answer:**\n\n> {answer}")

    save_to_cache(question, answer, used_chunks)

    with st.expander("📦 View Cached History"):
        if CACHE_FILE and os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                lines = f.readlines()[-5:]  # show last 5
                for l in lines:
                    rec = json.loads(l)
                    st.markdown(f"**Q:** {rec['question']}\n\n> **A:** {rec['answer']}\n---")   

