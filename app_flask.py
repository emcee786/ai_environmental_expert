from flask import Flask, request, render_template, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_session import Session

# Import the run_rag function from rag.py
from rag import run_rag
from manage_datastore import generate_datastore

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'supersecretkey'
Session(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

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
    generate_datastore()
    app.run(debug=True, host='127.0.0.1', port=5000)
