import mindsdb_sdk
from datetime import datetime
import numpy as np
import time
import platform
import psutil

# -----------------------
# 🔗 Connect to MindsDB
# -----------------------
server = mindsdb_sdk.connect('http://127.0.0.1:47334')

# -----------------------
# 📥 Ingestion Benchmark
# -----------------------
print("🚀 Measuring Knowledge Base ingestion time...")

kb_query = "DESCRIBE KNOWLEDGE_BASE mindsdb.customer_tickets_kb;"
query_result = server.query(kb_query).fetch()

if len(query_result) == 0:
    print("⚠️ No ingestion record found for the knowledge base.")
else:
    row = query_result.iloc[0]
    start_time = datetime.fromisoformat(row['INSERT_STARTED_AT'])
    end_time = datetime.fromisoformat(row['INSERT_FINISHED_AT'])
    processed_rows = int(row['PROCESSED_ROWS'])

    ingestion_time = (end_time - start_time).total_seconds()
    time_per_1k = ingestion_time / (processed_rows / 1000)

    print("\n✅ KB Ingestion Metrics:")
    print(f"📥 Total Ingestion Time: {ingestion_time:.2f} seconds")
    print(f"🔢 Rows Processed: {processed_rows}")
    print(f"🧮 Time per 1K Rows: {time_per_1k:.4f} seconds")

# -----------------------
# ⏱️ Query Latency Benchmark
# -----------------------
print("\n📈 Running query latency benchmarks...")

latency_query = """
SELECT metadata->>'ticket_id', metadata->>'ticket_subject'
FROM customer_tickets_kb
WHERE MATCH('internet issue')
LIMIT 3;
"""

latencies = []
for _ in range(50):
    start = time.perf_counter()
    _ = server.query(latency_query).fetch()
    end = time.perf_counter()
    latencies.append((end - start) * 1000)  # Convert to ms

avg_latency = np.mean(latencies)
p95_latency = np.percentile(latencies, 95)
p99_latency = np.percentile(latencies, 99)

print("\n⚡ Query Latency Benchmarks (50 queries):")
print(f"🔁 Average Latency: {avg_latency:.2f} ms")
print(f"📌 95th Percentile Latency: {p95_latency:.2f} ms")
print(f"📌 99th Percentile Latency: {p99_latency:.2f} ms")

# -----------------------
# 🖥️ System Environment Info
# -----------------------
print("\n🖥️ Environment Info:")
print("🧠 OS:", platform.system(), platform.release())
print("🖥️ CPU:", platform.processor())
print("💾 RAM:", round(psutil.virtual_memory().total / 1e9, 2), "GB")
print("🧪 MindsDB version: Run `SELECT version();` manually in MindsDB SQL console")
