from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

# Import the run_rag function from rag.py
from rag import run_rag

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('prompt', '')

    if not user_input:
        return jsonify({'response': 'Please provide a prompt.'}), 400

    try:
        # Call the run_rag function
        response, source = run_rag(user_input)
        return jsonify({'response': response, 'source': source})
    except Exception as e:
        return jsonify({'response': 'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
