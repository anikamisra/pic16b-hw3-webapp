# app.py file

from flask import Flask, request, render_template
import sqlite3
from flask import g
import random 
  
def get_message_db():
    """
    handles database creation for messages  
    """
    # check if message_db exists
    if 'message_db' not in g:
        # connect database 
        g.message_db = sqlite3.connect('messages_db.sqlite')
    cursor = g.message_db.cursor()

    # check for messages table  
    cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, handle TEXT, message TEXT)')
    return g.message_db


def insert_message(request):
    """
    insert message into database after user submission 
    """
    # connect database 
    db = get_message_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO messages (handle, message) VALUES (?, ?)', (request.form['user'], request.form['message']))
    # save 
    db.commit()
    # close the database connection 
    db.close()

def random_messages(n):
    """
    returns n (or fewer) random messages for viewing 
    """
    # connect database and get messages
    db = get_message_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM messages')
    messages = cursor.fetchall()
    # close connection 
    db.close()
    # return n messages (or, fewer if there aren't n messages)
    return random.sample(messages, min(n, len(messages)))


# create flask web server instance 
app = Flask(__name__)

# url route function for home page   
@app.route('/', methods=['GET'])
def home():
    # render submit.html page 
    return render_template('base.html')

# url route function for submit page  
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    message = None
    user = None
    # handle user posting 
    if request.method == 'POST':
        user = request.form['user']
        message = request.form['message']
        # call insert_message function 
        insert_message(request)
    return render_template('submit.html', user=user, message=message)

#  url route function for view messages page 
@app.route('/messages', methods=['GET'])
def messages(): 
    # generate 5 random messages to view 
    messages = random_messages(5)
    return render_template('view.html', messages=messages)
