import os
from flask import Flask, request, Response
from flask_mail import Mail
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from functools import wraps
from logging.config import fileConfig
from json import dumps

from services.users import register_user, login_user, forgot_password, change_password, edit_profile, get_user_detail, logout_user
from services.token import decode_jwt

listen = ['high', 'default', 'low']

app = Flask(__name__)
fileConfig('logging.cfg')
# ref for log  https://www.scalyr.com/blog/getting-started-quickly-with-flask-logging/

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

RESPONSE_HEADERS = {
        'Access-Control-Allow-Origin': '*',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy' : "default-src 'self'",
        'X-Content-Type-Options' : 'nosniff',
        'X-Frame-Options' : 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block'
    }

mail = Mail(app)
CORS(app)
bcrypt = Bcrypt(app)

MONGODB_URI = os.environ.get('MONGODB_URI_PART1') # add db url
client = MongoClient(MONGODB_URI + '&w=majority')
database = client.rentalvista

def authentication(auth):
    @wraps(auth)
    def token_auth(*args, **kwargs):
        try:
            # print(request.json)
            token = request.headers['Authorization']

            if not token:
                return dumps({"msg": "Please Login First!"}), 401
            
            token_data = decode_jwt(token)
            if token_data == "Signature expired. Please log in again." or token_data == 'Invalid token. Please log in again.':
                return dumps({"msg": "Please Login First!"}), 401
            
            if database.deniedTokens.count_documents({"token": token}) != 0:
                return dumps({"msg": "Please Login First!"}), 401

            return auth(*args, **kwargs)
        except Exception as e:
            return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500

    return  token_auth


@app.route("/", methods=["GET"])
def index():
    app.logger.info('Processing Index')
    # !ref: https://flask.palletsprojects.com/en/1.1.x/api/#response-objects
    response = Response(headers=RESPONSE_HEADERS, content_type='application/json')
    response.data = dumps({"msg":"HI"})
    response.status_code = 500
    print(response)
    return response

@app.route("/users/signup", methods=["POST"])
def signup():
    app.logger.info('Processing Signup...')
    user = database.user
    try:
        data = request.json['data']
        temp = data['name']
    except:
        data = request.json
    res = register_user(data["name"], data["email"], data["password"], data["contact"], user, bcrypt)
    response = Response(headers=RESPONSE_HEADERS, content_type='application/json')
    response.data = res[0]
    response.status_code = res[1]
    print(response)
    return response

@app.route("/users/login", methods=["POST"])
def login():
    app.logger.info('Processing Login...')
    user = database.user
    print(request.json)
    try:
        data = request.json['data']
        temp = data['email']
    except:
        data = request.json
    res = login_user(data['email'], data['password'], user, bcrypt)
    response = Response(headers=RESPONSE_HEADERS, content_type='application/json')
    response.data = res[0]
    response.status_code = res[1]
    # print(response)
    return response

@app.route("/users/forgot", methods=["POST"])
def forgot():
    app.logger.info('Processing Forgot Password...')
    user = database.user
    try:
        data = request.json['data']
        temp = data['email']
    except:
        data = request.json
    res = forgot_password(data['email'], user, mail, bcrypt)
    response = Response(headers=RESPONSE_HEADERS, content_type='application/json')
    response.data = res[0]
    response.status_code = res[1]
    return response

@app.route("/users/change", methods=["POST"])
@authentication
def change():
    app.logger.info('Processing Change Password...')
    token = request.headers['Authorization']
    user = database.user
    try:
        data = request.json['data']
        temp = data['password']
        print(data)
    except:
        data = request.json
        print(data)
    res = change_password(token, data['password'], data['new_password'], user, bcrypt)
    response = Response(headers=RESPONSE_HEADERS, content_type='application/json')
    response.data = res[0]
    response.status_code = res[1]
    return response

@app.route("/users/user", methods=["POST"])
@authentication
def user_detail():
    app.logger.info('Processing Find User...')
    token = request.headers['Authorization']
    user = database.user
    res = get_user_detail(token, user)
    response = Response(headers=RESPONSE_HEADERS, content_type='application/json')
    response.data = res[0]
    response.status_code = res[1]
    return response

@app.route("/users/edit", methods=["POST"])
@authentication
def edit():
    app.logger.info('Processing Edit Profile...')
    token = request.headers['Authorization']
    user = database.user
    try:
        data = request.json['data']
        temp = data['name']
    except:
        data = request.json
    res = edit_profile(token, data['name'], data['contact'], user)
    response = Response(headers=RESPONSE_HEADERS, content_type='application/json')
    response.data = res[0]
    response.status_code = res[1]
    return response

@app.route("/users/logout", methods=["POST"])
@authentication
def logout():
    app.logger.info('Processing Logout...')
    token = request.headers['Authorization']
    # print(token)
    user = database.user
    deniedToken = database.deniedTokens
    res = logout_user(token, user, deniedToken)
    response = Response(headers=RESPONSE_HEADERS, content_type='application/json')
    response.data = res[0]
    response.status_code = res[1]
    return response



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
