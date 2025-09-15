from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import flask, flask_socketio
import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=base_dir)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

socketio = SocketIO(app)

def get_db_connection():
    conn = sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row
    return conn

# create table if not exists
with get_db_connection() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule/index.html')

@app.route('/summary')
def summary():
    return render_template('summary/index.html')

@app.route('/old-exam')
def old_exam():
    return render_template('old-exam/index.html')

@app.route('/old-exam/1-1-f')
def old_exam_1_1_f():
    return render_template('old-exam/1-1-f/index.html')
    

@app.route('/chat')
def chat():
    return render_template('chat/index.html')

@app.route('/<path:path>')
def get_file(path):
    file_path = os.path.join(base_dir, path)
    if os.path.isfile(file_path):
        return flask.send_file(file_path)
    return 'File not found', 404

@socketio.on('connect')
def handle_connect(*args):
    print('Client connected')
    with get_db_connection() as conn:
        messages = conn.execute("SELECT * FROM messages ORDER BY timestamp DESC LIMIT 100").fetchall()
        messages = [dict(row) for row in messages[::-1]]
        emit('initial_messages', messages)

@socketio.on('message')
def handle_message(data):
    print(data)
    user, message = data['user'], data['message']
    with get_db_connection() as conn:
        conn.execute("INSERT INTO messages (user, message) VALUES (?, ?)", (user, message))
        conn.commit()
        emit('new_message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)