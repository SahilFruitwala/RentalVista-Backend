from os import environ
from flask import Flask, jsonify, request, flash
from flask_mail import Mail
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from services.users import register_user, login_user, forgot_password, change_password, edit_profile
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)
CORS(app)
bcrypt = Bcrypt(app)

URI = environ.get('URI') # add db url
client = MongoClient(URI)
database = client.rentalvista


@app.route("/signup", methods=["POST"])
def signup():
    user = database.user
    data = request.json
    print(data)
    return register_user(data["name"], data["email"], data["password"], data["contact"], user, bcrypt)

@app.route("/login", methods=["POST"])
def login():
    user = database.user
    data = request.json
    return login_user(data["email"], data["password"], user, bcrypt)

@app.route("/forgot", methods=["POST"])
def forgot():
    user = database.user
    data = request.json
    return forgot_password(data['email'], user, mail, bcrypt)

@app.route("/change", methods=["POST"])
def change():
    user = database.user
    data = request.json
    return change_password(data['token'], data['password'], data['new_password'], user, bcrypt)

@app.route("/edit", methods=["POST"])
def edit():
    token = request.headers['Authorization']
    user = database.user
    data = request.json
    print(token)
    print(data)
    return edit_profile(token, data['name'], data['contact'], user)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)