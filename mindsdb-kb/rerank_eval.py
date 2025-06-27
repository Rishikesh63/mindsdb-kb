import mindsdb_sdk
import pandas as pd
from termcolor import cprint


server = mindsdb_sdk.connect('http://127.0.0.1:47334')

# -----------------------
# 🧠 Configuration
# -----------------------
reranked_kb = 'customer_tickets_kb'
baseline_kb = 'customer_support_tickets_no_rerank_kb'
test_queries = [
    "Internet keeps disconnecting every 10 minutes",
    "Delivery marked complete but not received",
    "App crashes when I open camera",
    "Need refund for damaged item",
    "Payment was successful but no confirmation received"
]
limit = 3

# -----------------------
# 📊 Comparison Function
# -----------------------
def run_and_compare(query):
    rerank_sql = f"""
        SELECT metadata->>'ticket_id' AS ticket_id,
               metadata->>'ticket_subject' AS subject,
               metadata->>'ticket_description' AS description,
               relevance
        FROM {reranked_kb}
        WHERE MATCH('{query}')
        ORDER BY relevance DESC
        LIMIT {limit};
    """

    baseline_sql = f"""
        SELECT metadata->>'ticket_id' AS ticket_id,
               metadata->>'ticket_subject' AS subject,
               metadata->>'ticket_description' AS description,
               relevance
        FROM {baseline_kb}
        WHERE MATCH('{query}')
        ORDER BY relevance DESC
        LIMIT {limit};
    """

    reranked_results = server.query(rerank_sql).fetch()
    baseline_results = server.query(baseline_sql).fetch()

    return query, pd.DataFrame(reranked_results), pd.DataFrame(baseline_results)

# -----------------------
# 📋 Execute Comparisons
# -----------------------
comparative_report = []

for query in test_queries:
    try:
        query_text, reranked, baseline = run_and_compare(query)
        comparative_report.append({
            'query': query_text,
            'reranked': reranked,
            'baseline': baseline
        })
    except Exception as e:
        comparative_report.append({
            'query': query,
            'reranked': pd.DataFrame(),
            'baseline': pd.DataFrame(),
            'error': str(e)
        })

# -----------------------
# 📄 Print Side-by-Side Results
# -----------------------
for entry in comparative_report:
    query = entry['query']
    print(f"\n🔎 Query: {query}")
    print("-" * 80)
    if 'error' in entry:
        cprint(f"❌ Error: {entry['error']}", 'red')
        continue

    reranked_df = entry['reranked']
    baseline_df = entry['baseline']

    print(f"{'RERANKED RESULTS':<40} | {'BASELINE RESULTS':<40}")
    print(f"{'-'*40} | {'-'*40}")

    max_rows = max(len(reranked_df), len(baseline_df))
    for i in range(max_rows):
        left = f"[{i+1}] "
        if i < len(reranked_df):
            subj = reranked_df.iloc[i].get('subject', '')
            left += (subj[:35] if isinstance(subj, str) else 'N/A')
        else:
            left += " " * 35

        right = f"[{i+1}] "
        if i < len(baseline_df):
            subj = baseline_df.iloc[i].get('subject', '')
            right += (subj[:35] if isinstance(subj, str) else 'N/A')
        else:
            right += " " * 35

        print(f"{left:<40} | {right:<40}")

    print("\n📝 Descriptions Comparison:")
    for i in range(limit):
        if i < len(reranked_df):
            desc = reranked_df.iloc[i].get('description', '')
            cprint(f"[Reranked #{i+1}] {desc}", 'green')
        if i < len(baseline_df):
            desc = baseline_df.iloc[i].get('description', '')
            cprint(f"[Baseline #{i+1}] {desc}", 'yellow')
        print("-" * 80)

print("\n✅ Reranking comparison complete. Analyze the side-by-side differences above.")
