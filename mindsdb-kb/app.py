import streamlit as st
import mindsdb_sdk

# Connect to MindsDB
server = mindsdb_sdk.connect('http://127.0.0.1:47334')
agent_name = 'ticket_support_agent'

st.title("🎯 Ask the Customer Support Agent")

question = st.text_input("Ask your question:")

if st.button("Ask"):
    if question:
        try:
            query = f"""
                SELECT answer 
                FROM {agent_name}
                WHERE question = "{question}"
            """
            result = server.query(query).fetch()

            if not result.empty:
                answer = result.iloc[0]['answer']
            else:
                answer = "🤷 No response found."

            st.markdown(f"**Answer:** {answer}")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
    else:
        st.warning("Please enter a question first.")
