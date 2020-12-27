from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
from app import records
from app import notesDB
from app import texts
import uuid
from datetime import datetime
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import unicodedata


class User:

    def login(self):
        user = records.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            session['key'] = request.form.get('password')
            return self.start_session(user)
           
        return jsonify({"error": "Invalid login credentials"}), 401

    def start_session(self, user):
        del user['password']
        session['logged_in']=True
        session['chosenNote'] = ""
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        if (request.form.get('password') != request.form.get('confirm-password')):
            return jsonify({"error": "Passwords don't match"}), 400
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')        
            }
        session['key'] = user['password']
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if records.find_one({"email":user['email']}):
            return jsonify({"error": "Email already in use, please try a different email."}), 400

        if records.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Something went wrong, please try again"}), 400
    
    def signout(self):
        session.clear()
        return redirect('/')
    
    

    def createNote(self):
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

        f=Fernet(key)
        note = {
            "_id": uuid.uuid4().hex,
            "title": request.form.get('title'),
            "time": datetime.now(),
            "text": f.encrypt(request.form.get('text').encode('utf-8')),
            "email": session['user']['email'],
            "color": request.form.get('color')
            }
        # print(type(request.form.get('text').encode()))
        # print(type(note['text']))
        print(note['color'])
        notesDB.insert_one(note)
        return jsonify(note), 200

    def delete(self):
        # print("HI")
        print(unicodedata.normalize('NFKD', request.args.get("info")).encode('ascii', 'ignore')[2:-1:])
        # print(type(request.args.get("info")))
        # print (notesDB.find_one({"_id": unicodedata.normalize('NFKD', request.args.get("info")).encode('ascii', 'ignore')[3:-2:]}))
        note = notesDB.find_one({"_id": unicodedata.normalize('NFKD', request.args.get("info")).encode('ascii', 'ignore')})
        # print(note)
        texts.pop(str(note['_id']))
        # print(texts)
        notesDB.delete_one(note)
        return jsonify(session['user']), 200

    def open(self):
        # print(unicodedata.normalize('NFKD', request.args.get("info")).encode('ascii', 'ignore'))
        session['chosenNote'] = notesDB.find_one({"_id": unicodedata.normalize('NFKD', request.args.get("info")).encode('ascii', 'ignore')})
        return jsonify(session['chosenNote']), 200


    def editNote(self):
        print("cat")
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

        f=Fernet(key)
        edit = {
            "title": request.form.get('title'),
            "text": f.encrypt(request.form.get('text').encode('utf-8')),
            }
        notesDB.update_one({"_id":session['chosenNote']['_id']}, {'$set': edit})
        # print(type(request.form.get('text').encode()))
        # print(type(note['text']))
        return jsonify(session['user']), 200