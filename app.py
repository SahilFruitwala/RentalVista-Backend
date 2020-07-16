import os
from flask import Flask, jsonify, request, flash
from flask_mail import Mail
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import json
from functools import wraps

from services.users import register_user, login_user, forgot_password, change_password, edit_profile, get_user_detail, logout_user
from services.token import decode_jwt


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)
CORS(app)
bcrypt = Bcrypt(app)

MONGODB_URI = os.environ.get('MONGODB_URI_PART1') # add db url
client = MongoClient(MONGODB_URI + '&w=majority')
database = client.rentalvista

def authentication(auth):
    @wraps(auth)
    def token_auth(*args, **kwargs):
        token = request.headers['Authorization']

        if not token:
            return jsonify({"msg": "Please Login First!"}), 403
        
        token_data = decode_jwt(token)
        if token_data == "Signature expired. Please log in again." or token_data == 'Invalid token. Please log in again.':
            return jsonify({"msg": "Please Login First!"}), 403
        
        if database.deniedTokens.count_documents({"token": token}) != 0:
            return jsonify({"msg": "Please Login First!"}), 403

        return auth(*args, **kwargs)

    return  token_auth

@app.route("/", methods=["GET"])
def index():
    return "HELLo"

@app.route("/users/signup", methods=["POST"])
def signup():
    user = database.user
    data = request.json
    print(data)
    return register_user(data["name"], data["email"], data["password"], data["contact"], user, bcrypt)

@app.route("/users/login", methods=["POST"])
def login():
    user = database.user
    data = request.json
    return login_user(data["email"], data["password"], user, bcrypt)

@app.route("/users/forgot", methods=["POST"])
def forgot():
    user = database.user
    data = request.json
    return forgot_password(data['email'], user, mail, bcrypt)

@app.route("/users/change", methods=["POST"])
@authentication
def change():
    token = request.headers['Authorization']
    user = database.user
    data = request.json
    return change_password(token, data['password'], data['new_password'], user, bcrypt)

@app.route("/users/user", methods=["POST"])
@authentication
def user_detail():
    token = request.headers['Authorization']
    user = database.user
    return get_user_detail(token, user)

@app.route("/users/edit", methods=["POST"])
@authentication
def edit():
    token = request.headers['Authorization']
    user = database.user
    data = request.json
    return edit_profile(token, data['name'], data['contact'], user)

@app.route("/users/logout", methods=["POST"])
@authentication
def logout():
    token = request.headers['Authorization']
    user = database.user
    deniedToken = database.deniedTokens
    return logout(token, user, deniedToken)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

# !Done TODO: 0. Create a logout method
# !Done TODO: 1. Create a deniedTokens tokens 
# !Done TODO: 2. on logout add token to deniedTokens 
# !Done TODO: 3. on logout clear token from user 
# !Done TODO: 3. check token if token is in deniedTokens or not for services which needs authentication