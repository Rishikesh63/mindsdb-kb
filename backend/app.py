from flask import Flask, request, jsonify, render_template_string
import mindsdb_sdk

app = Flask(__name__)
server = mindsdb_sdk.connect('http://127.0.0.1:47334')
agent_name = 'ticket_support_agent'

FORM_HTML = """
<!DOCTYPE html>
<html>
<head><title>MindsDB Agent</title></head>
<body>
  <h2>Ask the MindsDB Agent</h2>
  <form method="get" action="/ask">
    <input type="text" name="question" placeholder="Your question here" size="50">
    <button type="submit">Ask</button>
  </form>
  {% if answer %}
  <h3>Answer:</h3>
  <p>{{ answer }}</p>
  {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    return "✅ MindsDB Agent Server is Running!"

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    question = request.args.get('question') if request.method == 'GET' else request.get_json().get('question')
    if not question:
        return render_template_string(FORM_HTML)

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

        if request.method == 'GET':
            return render_template_string(FORM_HTML, answer=answer)

        return jsonify({'answer': answer})

    except Exception as e:
        if request.method == 'GET':
            return render_template_string(FORM_HTML, answer=f"⚠️ Error: {e}")
        return jsonify({'error': str(e)}), 500
