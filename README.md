# 🧠 MindsDB KB App — Customer Support Ticket Analyzer

This project is built for the MindsDB **Quest-19: Stress-Test Knowledge Bases** challenge. It demonstrates a complete end-to-end pipeline to build, populate, and query a Knowledge Base (KB) using MindsDB and local Ollama models.

---

## 📌 Overview

The application performs the following:

✅ Creates a **Knowledge Base** (`customer_tickets_kb`)  
✅ Ingests a **CSV dataset** (`customer_support_tickets.csv`) with **metadata columns**  
✅ Creates a **vector index** on the KB for semantic search  
✅ Sets up an **AI Model** (retrieval-based using Ollama's LLaMA3)  
✅ Connects the model to an **Agent** (`ticket_support_agent`)  
✅ Demonstrates **semantic queries** using the KB  
✅ Designed to support integration with CLI/Web/API easily

---

## 📂 Dataset

We use a dataset named `customer_support_tickets.csv` containing 8,000+ rows of customer issues and ticket information.

---

## 🚀 Requirements

- Python 3.9+
- MindsDB running locally (`docker` or `source`)
- Ollama running locally with `llama3` and `llama2` pulled
- Install dependencies:

```bash
pip install mindsdb_sdk pandas
