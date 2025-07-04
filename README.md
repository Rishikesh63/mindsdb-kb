# 🧠 MindsDB KB App — Customer Support & Movie Q&A Agent

This project is built for the MindsDB **Quest-19: Stress-Test Knowledge Bases** challenge. It demonstrates a complete end-to-end pipeline using **MindsDB**, **local Ollama LLMs**, and **Streamlit UI** for:

- 📊 Customer support ticket analysis  
- 🎬 Movie-related question answering  
- ✅ Accuracy benchmarking

[![Watch the video](https://img.youtube.com/vi/m-U5XL72mJ8/0.jpg)](https://www.youtube.com/watch?v=m-U5XL72mJ8&t=22s)


---

## 📌 Overview

This application performs the following:

### ✅ Customer Support Agent
- Creates a **Knowledge Base** (`customer_tickets_kb`)
- Ingests a **CSV dataset** (`customer_support_tickets.csv`) with **metadata**
- Builds a **vector index** for semantic search
- Creates an AI model using **LLaMA3** via Ollama
- Deploys a **retrieval-augmented agent** (`ticket_support_agent`)
- Supports interactive Q&A and summarization of customer issues

### ✅ Movie Expert Agent
- Loads a **summary-based knowledge base** (`movies_kb`)
- Creates an agent (`movie_expert_agent`) using **LLaMA2**
- Answers plot, character, and theme-related movie questions

### ✅ Benchmarking
- Measures ingestion time, semantic query latency, and p95/p99 response delays
- Outputs structured `.md` reports under `benchmarks/`

---

## 📂 Dataset

### 1. `customer_support_tickets.csv`  
Contains  **8,469 support tickets** with metadata:
- Ticket ID, Subject, Description
- Priority, Status, Type, Channel

### 3. `imdb_movies_prepared.csv`  
Contains:

- Movie title, genre, actors, year, rating
- ✅ Original dataset size: 238,256 rows  
- ✅ After removing duplicates: 161,765 rows  
- ✅ Saved to `imdb_movies_prepared.csv` for clean ingestion


---

## 🧪 Project Structure

```bash
cd mindsdb-kb
```

---

## 🚀 How to Run

### 1️⃣ Install dependencies (Python ≥ 3.10)
```bash
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2️⃣ Launch the Streamlit UI

#### 🧠 Customer Support Agent:
```bash
streamlit run app.py
```

#### 🎬 Movie QA Agent:
```bash
streamlit run movie.py
```

### 3️⃣ Run Benchmarking
```bash
python benchmark.py
```

---

## 🔍 What’s Measured in Benchmarks?

Each `.md` report includes:

| Category            | Metric                              |
|---------------------|--------------------------------------|
| ⏱️ Ingestion Time    | Total seconds + time per 1K rows     |
| ⚡ Query Latency     | Average, p95, p99 response times     |


---

Built with ❤️ using MindsDB, Ollama, Streamlit, and Python.
