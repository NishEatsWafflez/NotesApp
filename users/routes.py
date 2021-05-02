from flask import Flask
from app import app
from users.models import User

@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/login', methods=['POST'])
def login():
    return User().login()

@app.route('/new', methods=['POST'])
def newNote():
    return User().createNote()

@app.route('/edits', methods=['POST'])
def edits():
    return User().editNote()

@app.route('/delete', methods=['GET'])
def delete():
    # print("hi")
    # print(request.args.get("info"))
    return User().delete()

@app.route('/editing', methods=['GET'])
def editing():
#     # print("hi")
#     # print(request.args.get("info"))
    return User().open()



