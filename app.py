from flask import Flask, render_template, redirect, session
from functools import wraps
from bson.objectid import ObjectId
import dns
import os
import pymongo
from pymongo import MongoClient
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from dotenv import load_dotenv, find_dotenv

# from app import chosenNote

# from users.models import User

app = Flask(__name__)
app.secret_key = b'\xc5\x19\xb95\x91L\x9e\x83\xa5\xd5\xad)\xd0\x8f\x02w'
texts = {}
info = {}
load_dotenv(find_dotenv())

MONGO = os.getenv("MONGO")
client = MongoClient(MONGO)
db = client.get_database('loginInfo')
records = db.login_db
notesDB = db.notes_db

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap


from users import routes

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    notes = notesDB.find({'email':session['user']['email']})
    password = session['key'].encode()  # Convert to type bytes
    salt = b'\xb7\xe799d\x8864\xf9\xa4P\xea\x15\xb3\x8e)'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    f = Fernet(key)
    for note in notes:
        infos = []
        infos.append(note['title'])
        # print(type(note['text']))
        b = note['text'].encode('utf-8')
        # print(type(b"hi"))
        note['text'] = f.decrypt(b)
        infos.append(note['text'])
                # print(note['text'])
        texts[note['_id']]= infos
        # print (infos.keys())
        # print(infos)
        # info.pop(note['title'])
        # print(notes)

        # print(1)
        # print(type(note['text']))
        # decoded_value = note['text'].serialize()
        # decoded_value = bytes(decoded_value)
        # print(type(decoded_value))
        # note['text'] = f.decrypt(note['text'].encode)
    # print(session['user']['email'])
    for x in texts.copy():
        check = notesDB.find_one({'_id':x})
        if check['email'] != session['user']['email']:
            texts.pop(x)
    print (texts)
    # print(texts.keys())
    return render_template('dashboard.html', notes=texts.items())
    # return render_template('dashboard.html')

@app.route('/register/')
def register():
    return render_template('home.html')

@app.route('/edit/')
@login_required
def edit():
    password = session['key'].encode()  # Convert to type bytes
    salt = b'\xb7\xe799d\x8864\xf9\xa4P\xea\x15\xb3\x8e)'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    f = Fernet(key)
    # print(type(note['text']))
    b = session['chosenNote']['text'].encode('utf-8')
    # print(type(b"hi"))
    session['chosenNote']['text'] = f.decrypt(b)
    text = session['chosenNote']['text']
    # print(note['text'])
    # print(session['chosenNote']['text'])
    return render_template('edit.html', note = session['chosenNote'], text = text)

@app.route('/view/')
@login_required
def view():
    password = session['key'].encode()  # Convert to type bytes
    salt = b'\xb7\xe799d\x8864\xf9\xa4P\xea\x15\xb3\x8e)'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    f = Fernet(key)
    # print(type(note['text']))
    b = session['chosenNote']['text'].encode('utf-8')
    # print(type(b"hi"))
    session['chosenNote']['text'] = f.decrypt(b)
    text = session['chosenNote']['text']
    # print(note['text'])
    # print(session['chosenNote'])
    return render_template('view.html', note = session['chosenNote'], text = text)
