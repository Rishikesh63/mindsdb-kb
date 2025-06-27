import mindsdb_sdk
import pandas as pd

server = mindsdb_sdk.connect('http://127.0.0.1:47334')


def ensure_table():
    df = pd.read_csv('customer_support_tickets.csv')
    files_db = server.databases.files
    existing_tables = [t.name for t in files_db.tables.list()]
    if 'customer_support_tickets' not in existing_tables:
        files_db.tables.create('customer_support_tickets', df)
        print("✅ Table created")
    else:
        print("ℹ️ Table already exists")


def setup_agent():
    agent_name = 'ticket_support_agent'
    model_name = 'ticket_model'
    kb_name = 'customer_tickets_kb'

    ensure_table()

    # Create model only if it doesn't already exist
    try:
        server.models.get(model_name)
        print(f"ℹ️ Model '{model_name}' already exists.")
    except:
        try:
            server.models.create(
                name=model_name,
                predict='answer',
                mode='retrieval',
                engine='ollama',
                model_name='llama3',
                provider='ollama',
                base_url='http://127.0.0.1:11434',
                knowledge_base=kb_name,
                prompt_template='''
Use the customer_tickets_kb to answer user queries about customer issues, tickets, complaints.
                '''
            )
            print(f"✅ Model '{model_name}' created.")
        except Exception as e:
            print("❌ Failed to create model:", e)

    # Create agent only if it doesn't already exist
    try:
        server.agents.get(agent_name)
        print(f"ℹ️ Agent '{agent_name}' already exists.")
    except:
        try:
            server.agents.create(
                name=agent_name,
                model=model_name
            )
            print("✅ Agent created.")
        except Exception as e:
            print("❌ Failed to create agent:", e)


if __name__ == "__main__":
    setup_agent()
