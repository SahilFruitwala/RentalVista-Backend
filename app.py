from configparser import ConfigParser
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from services.users import register_user, validate_user
import json

# Read Credential File
config = ConfigParser()
config.read('config.ini')

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)