from configparser import ConfigParser
from flask import Flask, jsonify, request
from flask.ext.pymongo import PyMongo

# Create an instance of class, first argument is name of application
app = Flask(__name__)

# Read Creadential File
config = ConfigParser()
config.read('config.ini')

URL = config.get('MongoDB', 'URL') # add db url
client = pymongo.MongoClient()
db = client.Tutorial5

@app.route("/", methods=["GET"])
@app.route("/users", methods=["GET"])
def getAllUsers():
    user_collection = db.users
    users = user_collection.find({}, {'_id': 0})
    users_list = list(users)
    print(users_list)
    return {'response': users_list}


@app.route("/getUser", methods=["GET"])
def getUser():
    get_user_data = request.get_json()
    username = str(get_user_data["username"])
    user = db.users.find_one({"username": username}, {'_id': 0})
    users_list = []
    users_list.append(user)
    return {'response': users_list}


@app.route("/put", methods=["PUT"])
def put():
    get_user_data = request.get_json()
    username = str(get_user_data["username"])
    new_name = get_user_data["newname"]
    if not get_user_data:
        err = {'ERROR': 'No data passed'}
        return jsonify(err)
    else:
        # If username is passed and is found in db, replace it with the new value
        if username:
            if db.users.find_one({'username': username}):
                db.users.update_one({'username': username}, {
                                    "$set": {'username': new_name}})
                return {'response': 'Username:'+str(username)+' updated with username:'+str(new_name)}
            else:
                return {'Error': 'Username ' + str(username) + ' not found'}

        else:
            return {'response': 'Username missing'}

@app.route("/adduser", methods=["POST"])
def adduser():
    get_user_data = request.get_json()
    email = get_user_data["email"]
    username = get_user_data["username"]
    db.users.insert({'email': email,'username': username})
    return jsonify({'message': 'user created successfully...'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)