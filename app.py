# app.py file

from flask import Flask, request, render_template
import sqlite3
from flask import g
import random 

def get_message_db():
    if 'message_db' not in g:
        g.message_db = sqlite3.connect('messages_db.sqlite')
    cursor = g.message_db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, handle TEXT, message TEXT)')
    return g.message_db

def insert_message(request):
    db = get_message_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO messages (handle, message) VALUES (?, ?)', (request.form['user'], request.form['message']))
    db.commit()
    # close the database connection 
    #db.close()

def random_messages(n):
    db = get_message_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM messages')
    messages = cursor.fetchall()
    db.close()
    return random.sample(messages, min(n, len(messages)))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('submit.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    message = None
    user = None
    if request.method == 'POST':
        user = request.form['user']
        message = request.form['message']
        insert_message(request)
    return render_template('submit.html', user=user, message=message)

@app.route('/messages', methods=['GET'])
def messages(): 
    messages = random_messages(5)
    return render_template('view.html', messages=messages)

"""

@app.route('/', methods=['GET', 'POST'])
def submit():
    message = None
    user = None
    if request.method == 'POST':
        user = request.form['user']
        message = request.form['message']
        insert_message(request)
    return render_template('submit.html', user=user, message=message)

@app.route('/messages', methods=['GET'])
def messages():
    messages = fetch_messages()
    return render_template('messages.html', messages=messages)"""

"""@app.route('/messages', methods=['GET'])
def messages():
    messages = fetch_messages()
    return render_template('view.html', messages=messages)"""

"""
@app.route('/messages', methods=['GET'])
def messages(): 
    db = get_message_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM messages')
    messages = cursor.fetchall()
    return render_template('view.html', messages=messages)
"""
