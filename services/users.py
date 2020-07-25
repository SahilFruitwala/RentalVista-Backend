from .token import encode_jwt, decode_jwt
from flask import flash
from json import dumps
from flask_mail import Message
from .password_generator import generate_random_pass
from datetime import datetime
from bson.objectid import ObjectId

def register_user(name: str, email: str, password: str, contact:str, user, bcrypt) -> str:
    try:
        if user.count_documents({"email": email}) == 0:
            hashed_password = bcrypt.generate_password_hash(password)
            user_id = user.insert_one({"name":name, "email": email, "password": hashed_password, "contact": contact, "token": ""}).inserted_id
            return dumps({"msg" : 'Registration Success!'}) , 200

        return dumps({"msg" : "User Already Exist!"}) , 409
    except Exception as e:
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500

def login_user(email: str, password: str, user, bcrypt) -> str:
    try:
        if user.count_documents({"email": email}) == 0:
            return dumps({"msg":"User does not exist!"}), 401
    except Exception as e:
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500
    try:
        result = user.find_one({"email":email}, {"password": password, "_id":1})
        if compare_password(bcrypt, result['password'], password):
            token = encode_jwt(str(result['_id'])) # converted id into string then passed to encode_jwt
            user.update_one({"email" : email},{'$set': { "token" : token.decode('utf-8')}})
            return dumps({'msg': 'Login Success!', "token": token.decode('utf-8')}), 200 # need to decode JWT from bytes to string 

        return dumps({"msg" : "Email or Password is incorrect!"}), 406
    except Exception as e:
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500

def forgot_password(email: str, user, mail, bcrypt) -> str:
    try:
        if user.count_documents({"email": email}) == 0:
            return dumps({"msg": "User does not exist!"}), 401

        new_password = generate_random_pass()

        msg = Message('Reset Password', recipients=[email])
        msg.html = ('<h2>Password Reset</h2>' 
                    '<p>Your new password is <b>'+new_password+'</b></p>'
                    '<p><i><b>Note:</b>Do not Share this mail with anyone.</i></P>')
        mail.send(msg)
        flash(f'Reset Password sent to {email}.')
        
        hashed_password = bcrypt.generate_password_hash(new_password)
        user.update_one({"email" : email},{'$set': { "password" : hashed_password}})
        return dumps({"msg" : "Password Reset Success!"}) ,200
    except Exception as e:
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500

def change_password(token: str, password: str, new_password: str, user, bcrypt) -> str:
    try:
        user_data = user.find_one({"token":token}, {"password": password, "_id":0})
        if compare_password(bcrypt, user_data['password'], password):
            hashed_password = bcrypt.generate_password_hash(new_password)
            user.update_one({"token" : token},{'$set': { "password" : hashed_password}})
            return dumps({"msg" : "Password Changed!"}), 200
        return dumps({"msg" : 'Incorrect Current Password!'}), 406
    except Exception as e:
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500

def edit_profile(token: str, name: str, contact: str, user):
    try:
        user.update_one({"token" : token},{'$set': { "name" : name, "contact": contact}})
        updated_data = user.find_one({"token": token}, {"name": name, "contact": contact ,"_id":0})
        return dumps(updated_data), 200
    except Exception as e:
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500

def get_user_detail(token: str, user):
    try:
        data = user.find_one({"token": token}, {"name": 1, "email": 1, "contact": 1 ,"_id":0})
        return dumps(data), 200
    except Exception as e:
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500

def logout_user(token: str, user, deniedToken) -> str:
    token_data = decode_jwt(token)
    try:
        user.update_one({"_id" : ObjectId(token_data)},{'$set': {"token" : ""}})
        deniedToken.insert_one({"token": token, "denied_time": str(datetime.now())}).inserted_id
    except Exception as e:
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500
    return dumps({"msg": "Logout Success!"}), 200

def compare_password(bcrypt, hashed_password, password) -> bool:
    return bcrypt.check_password_hash(hashed_password, password)