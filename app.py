# Author: Sahil Fruitwala - B00844489
# Author: Naitik Prajapti - B00856835
# Author: Krupa Patel - B00828120
# Author: Gaurav Anand - B00832139
# Author: Amogh Adithya Bangalore - B00833535

import os
import pymongo
from flask import Flask, jsonify, request, flash, Response
from flask_mail import Mail
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from functools import wraps
from logging.config import fileConfig
from json import dumps
import base64

from services.users import register_user, login_user, forgot_password, change_password, edit_profile, get_user_detail, logout_user
from services.token import decode_jwt
from services.appointment import book_appointment
from services.post import add_post, get_rooms, delete_room, disable_room
from services.properties import get_all_properties

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
    'Content-Security-Policy': "default-src 'self'",
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block'
}

mail = Mail(app)
CORS(app)
bcrypt = Bcrypt(app)

MONGODB_URI = os.environ.get('MONGODB_URI_PART1')
client = MongoClient(MONGODB_URI + '&w=majority')

database = client.rentalvista

# Author: Sahil Fruitwala - B00844489
def authentication(auth):
    @wraps(auth)
    def token_auth(*args, **kwargs):
        try:
            app.logger.info('Authenticating User')
            token = request.headers['Authorization']

            if not token:
                app.logger.info('Checking Token Availability')
                return dumps({"msg": "Please Login First!"}), 401

            token_data = decode_jwt(token)
            if token_data == "Signature expired. Please log in again." or token_data == 'Invalid token. Please log in again.':
                app.logger.info('Validating Token')
                return dumps({"msg": "Please Login First!"}), 401

            if database.deniedTokens.count_documents({"token": token}) != 0:
                app.logger.info('Invalid Token Found')
                return dumps({"msg": "Please Login First!"}), 401

            return auth(*args, **kwargs)
        except Exception as e:

            app.logger.info('Exception Occurred in Token Validation')
            return dumps({"msg": 'Some internal error occurred!', "error": str(e)}), 500

    return token_auth

# Author: Sahil Fruitwala - B00844489
@app.route("/users/signup", methods=["POST"])
def signup():
    app.logger.info('Start Signup')
    user = database.user
    try:
        data = request.json['data']
        temp = data['name']
    except:
        data = request.json

    app.logger.info('Star Registering User')
    res = register_user(data["name"], data["email"],
                        data["password"], data["contact"], user, bcrypt)
    response = Response(headers=RESPONSE_HEADERS,
                        content_type='application/json')
    app.logger.info('End Registering User')
    response.data = res[0]
    response.status_code = res[1]
    app.logger.info('End Signup')
    return response

# Author: Gaurav Anand - B00832139
@app.route("/post/add", methods=["POST"])
def add_property():
    app.logger.info('Adding post')
    token = request.json['headers']['Authorization']
    rooms = database.rooms
    try:
        data = request.json['data']
    except:
        data = request.json
    res = add_post(token, data, rooms)
    response = Response(headers=RESPONSE_HEADERS,
                        content_type='application/json')
    response.data = res[0]
    response.status_code = res[1]
    return response

# Author: Gaurav Anand - B00832139
@app.route("/post/get", methods=["GET"])
def get_properties():
    app.logger.info('Getting all posts for user profile')
    token = request.headers['Authorization']
    rooms = database.rooms
    res = get_rooms(token, rooms)
    response = Response(headers=RESPONSE_HEADERS,
                        content_type='application/json')
    response.data = res[0]
    response.status_code = res[1]
    return response

# Author: Gaurav Anand - B00832139
@app.route("/post/update", methods=["POST"])
def disable():
    app.logger.info('Start Disabling Room')
    token = request.headers['Authorization']
    rooms = database.rooms
    try:
        data = request.json['data']
    except:
        data = request.json
    app.logger.info('Start Disabling Room Inner')
    res = disable_room(data['roomID'], data['disabled'], rooms)

    response = Response(headers=RESPONSE_HEADERS,
                        content_type='application/json')
    app.logger.info('End Disabling Room Inner')

    response.data = res[0]
    response.status_code = res[1]
    app.logger.info('End Disabling Room')
    return response

# Author: Gaurav Anand - B00832139
@app.route("/post/delete", methods=["DELETE"])
def delete_property():
    app.logger.info("Deleting property")
    token = request.headers['Authorization']
    rooms = database.rooms
    try:
        data = request.json['data']
    except:
        data = request.json
    res = delete_room(data['roomID'], rooms)
    response = Response(headers=RESPONSE_HEADERS,
                        content_type='application/json')
    response.data = res[0]
    response.status_code = res[1]
    return response

# Author: Sahil Fruitwala - B00844489
@app.route("/users/login", methods=["POST"])
def login():
    app.logger.info('Start Login')
    user = database.user
    try:
        data = request.json['data']
        temp = data['email']
    except:
        data = request.json
    app.logger.info('Start Credentials Verification')
    res = login_user(data['email'], data['password'], user, bcrypt)

    response = Response(headers=RESPONSE_HEADERS,
                        content_type='application/json')
    app.logger.info('End Credentials Verification')

    response.data = res[0]
    response.status_code = res[1]
    app.logger.info('End Login')
    return response

# Author: Sahil Fruitwala - B00844489
@app.route("/users/forgot", methods=["POST"])
def forgot():
    app.logger.info('Start Forgot Password')
    user = database.user
    try:
        data = request.json['data']
        temp = data['email']
    except:
        data = request.json
    app.logger.info('Start Forgot Password Inner')
    res = forgot_password(data['email'], user, mail, bcrypt)

    response = Response(headers=RESPONSE_HEADERS,
                        content_type='application/json')
    app.logger.info('End Forgot Password Inner')

    response.data = res[0]
    response.status_code = res[1]
    app.logger.info('End Forgot Password')
    return response

# Author: Sahil Fruitwala - B00844489
@app.route("/users/change", methods=["POST"])
@authentication
def change():
    app.logger.info('Start Change Password')
    token = request.headers['Authorization']
    user = database.user
    try:
        data = request.json['data']
        temp = data['password']
    except:
        data = request.json

    app.logger.info('Start Change Password Inner')
    res = change_password(
        token, data['password'], data['new_password'], user, bcrypt)
    response = Response(headers=RESPONSE_HEADERS,
                        content_type='application/json')
    app.logger.info('End Change Password Inner')

    response.data = res[0]
    response.status_code = res[1]
    app.logger.info('End Change Password')
    return response

# Author: Sahil Fruitwala - B00844489
@app.route("/users/user", methods=["GET"])
@authentication
def user_detail():
    app.logger.info('Start Fetching User')
    token = request.headers['Authorization']
    user = database.user
    app.logger.info('Start Fetching User Inner')
    res = get_user_detail(token, user)
    response = Response(headers=RESPONSE_HEADERS,
                        content_type='application/json')
    app.logger.info('End Fetching User Inner')

    response.data = res[0]
    response.status_code = res[1]
    app.logger.info('End Fetching User')
    return response

# Author: Sahil Fruitwala - B00844489
@app.route("/users/edit", methods=["POST"])
@authentication
def edit():
    app.logger.info('Start Edit Profile')
    token = request.headers['Authorization']
    user = database.user
    try:
        data = request.json['data']
        temp = data['name']
    except:
        data = request.json
    app.logger.info('Start Edit Profile Inner')
    res = edit_profile(token, data['name'], data['contact'], user)

    response = Response(headers=RESPONSE_HEADERS,
                        content_type='application/json')
    app.logger.info('End Edit Profile Inner')

    response.data = res[0]
    response.status_code = res[1]
    app.logger.info('End Edit Profile')
    return response

# Author: Sahil Fruitwala - B00844489
@app.route("/users/logout", methods=["GET"])
@authentication
def logout():
    app.logger.info('Start Logout')
    token = request.headers['Authorization']
    user = database.user
    deniedToken = database.deniedTokens
    app.logger.info('Start Logout Inner')
    res = logout_user(token, user, deniedToken)

    response = Response(headers=RESPONSE_HEADERS,
                        content_type='application/json')
    app.logger.info('End Logout Inner')

    response.data = res[0]
    response.status_code = res[1]
    app.logger.info('End Logout')
    return response

#Author: Amogh Adithya Bangalore - B00833535   
@app.route("/getblog", methods=["GET"])
def getblog():
    blog_collection = database.blogs
    blog = blog_collection.find({}, {'_id': 0})
    blog_list = list(blog)
    return jsonify(blog_list)
    
#Author: Amogh Adithya Bangalore - B00833535      
@app.route("/addblog", methods=["POST"])
def addblog():
    get_user_data = request.get_json()
    title = get_user_data["title"]
    author = get_user_data["author"]
    desc = get_user_data["desc"]
    if not get_user_data:
        err = {'ERROR': 'No data passed'}
        return jsonify(err)
    else:
        lastid = database.blogs.find().sort([("_id", -1)]).limit(1)
        print("Last id:", lastid)
        if (lastid):
            id = int(lastid[0]["id"]) + 1
        else:
            id = 1

        print(id)
        if database.blogs.find_one({'title': title}):
            return jsonify("Blog Title already present, cannot add")
        else:
            database.blogs.insert(
                {'id': str(id), 'title': title, 'author': author, 'desc': desc})
            return jsonify("User added successfully!..")

#Author: Amogh Adithya Bangalore - B00833535              
@app.route("/deleteblog", methods=["POST"])
def deleteblog():
    data = request.get_json()
    title = data["title"]
    author = data["author"]
    desc = data["desc"]
    if not data:
        err = {'ERROR': 'No data passed'}
        return jsonify(err)
    else:
        lastid = database.blogs.find().sort([("_id", -1)]).limit(1)
        id = int(lastid[0]["id"]) + 1

        print(id)
        if database.blogs.find_one({'title': title}):
            delb = database.blogs.find_one({'title': title})
            database.blogs.delete_one(delb)
            return jsonify("Blog deleted")
        else:
            return jsonify("Record not found!")

#Author: Amogh Adithya Bangalore - B00833535 
@app.route("/editblog", methods=["PUT"]) 
def editblog():
    data = request.get_json()
    title = data["title"]
    author = data["author"]
    desc = data["desc"]
    if not data:
        err = {'ERROR': 'No data passed'}
        return jsonify(err)
    else:
        # If Author is passed and is found in db, replace it with the new value
        if title:
            if database.blogs.find_one({'author': author}):
                database.blogs.update_one({'author': author}, {
                    "$set": {'title': title, 'desc': desc, 'author': author}})
                return jsonify('Blog updated Successfully!')
            else:
                return jsonify("Author not found")

#Author: Krupa Patel - B00828120
@app.route("/appointment/book", methods=["POST"])
def bookAppointment():
    app.logger.info("Booking an Appointment")
    data = request.get_json()
    # print(data)
    appointment = database.appointment
    adata = data['data']
    print(adata)
    res = book_appointment(adata, appointment)
    response = Response(headers=RESPONSE_HEADERS,
                        content_type='application/json')
    return response

#Author: Krupa Patel - B00828120
@app.route('/myappointment/<userId>', methods=['GET'])
def get_appointment(userId):
    app.logger.info("Getting Appointment")
    appointment = database.appointment
    data = appointment.find({"email": userId})
    appointments = []
    for i in data:
        data = {
            'postid': i['postid'],
            'date': i['date'],
            'time': i['time'],
            'email': i['email'],
            'owneremail': i['owneremail']
        }
        appointments.append(data)
        data = {}

    return json.dumps(appointments), 200

#Author: Harshitha M S - B00838019
@app.route("/getcomment", methods=["GET"])
def getcomment():
    app.logger.info("Getting comments")
    comment_collection = database.comments
    comment = comment_collection.find({}, {'_id': 0})
    comment_list = list(comment)
    return jsonify(comment_list)

#Author: Harshitha M S - B00838019
@app.route("/addcomment", methods=["POST"])
def addcomment():
    app.logger.info("Posting comment")
    data = request.get_json()
    comment = data["comment"]
    if not data:
        err = {'ERROR': 'No data passed'}
        return jsonify(err)
    else:
        lastid = database.comments.find().sort([("_id", -1)]).limit(1)
        if (lastid):
            id = int(lastid[0]["id"]) + 1
        else:
            id = 1
        database.comments.insert(
        {'id': str(id), 'comment': comment})
        return jsonify("Comment posted successfully!..")

#Author: Naitik Prajapti - B00856835
@app.route("/api/getrooms", methods=["GET"])
def getRoom():
    app.logger.info('Processing Get Rooms...')
    # Fetch Documents from collection rooms
    properties = database.rooms
    return get_all_properties(properties)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
