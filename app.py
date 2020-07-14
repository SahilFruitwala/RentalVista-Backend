from os import environ
from configparser import ConfigParser
from flask import Flask, jsonify, request, flash
from flask_mail import Mail
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from services.users import register_user, validate_user, forgot_pass
import json

# Read Credential File
config = ConfigParser()
config.read('config.ini')

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

URI = config.get('MongoDB', 'URI') # add db url
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
    return validate_user(data["email"], data["password"], user, bcrypt)

@app.route("/forgot", methods=["POST"])
def forgot():
    user = database.user
    data = request.json
    return forgot_pass(data['email'], user, mail, bcrypt)

# @app.route("/", methods=['GET'])
# def index():
#     # recipient = request.form['recipient']
#     recipient = 'sh941551@dal.ca'
#     msg = Message('Reset Password', recipients=[recipient])
#     # msg.body = ('Congratulations! You have sent a test email with' 
#     #             'Twilio SendGrid!')
#     msg.html = ('<h2>Password Reset</h2>' 
#             '<p>Your new password is <b>HEY</b></p>'
#             '<p><i><b>Note:</b>Do not Share this mail with anyone.</i></P>')
#     mail.send(msg)
#     flash(f'Reset Password sent to {recipient}.')
#     return "Done"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)