from .token import encode_jwt, decode_jwt
from flask import flash, jsonify
from flask_mail import Message
from .password_generator import generate_random_pass
from datetime import datetime


def register_user(name: str, email: str, password: str, contact:str, user, bcrypt) -> str:
    
    if user.count_documents({"email": email}) == 0:
        hashed_password = bcrypt.generate_password_hash(password)
        return str(user.insert_one({"name":name, "email": email, "password": hashed_password, "contact": contact, "token": ""}).inserted_id)
    
    return "User Already Exist!"

def login_user(email: str, password: str, user, bcrypt) -> str:
    
    if user.count_documents({"email": email}) == 0:
        return "User does not exist!"
    
    result = user.find_one({"email":email}, {"password": password, "_id":1})
    if bcrypt.check_password_hash(result['password'], password):
        print(type(result['_id']))
        token = encode_jwt(str(result['_id'])) # converted id into string then passed to encode_jwt
        user.update_one({"email" : email},{'$set': { "token" : token}})
        return {'msg': 'Login Success!', "token": token.decode('utf-8')} # need to decode JWT from bytes to string 

    return "Email or Password is incorrect!"

def forgot_password(email: str, user, mail, bcrypt) -> str:
    
    if user.count_documents({"email": email}) == 0:
        return "User does not exist!"

    new_password = generate_random_pass()

    msg = Message('Reset Password', recipients=[email])
    msg.html = ('<h2>Password Reset</h2>' 
                '<p>Your new password is <b>'+new_password+'</b></p>'
                '<p><i><b>Note:</b>Do not Share this mail with anyone.</i></P>')
    mail.send(msg)
    flash(f'Reset Password sent to {email}.')
    
    hashed_password = bcrypt.generate_password_hash(new_password)
    user.update_one({"email" : email},{'$set': { "password" : hashed_password}})
    return "Password Reset Success!"

def change_password(token: str, password: str, new_password: str, user, bcrypt) -> str:
    token = token.encode('utf-8')
    user_data = user.find_one({"token":token}, {"password": password, "_id":1})
    if bcrypt.check_password_hash(user_data['password'], password):
        hashed_password = bcrypt.generate_password_hash(new_password)
        user.update_one({"token" : token},{'$set': { "password" : hashed_password}})
        return "Password Changed!"
    return "Incorrect Current Password!"

def edit_profile(token: str, name: str, contact: str, user):
    try:
        token = token.encode('utf-8')
        user.update_one({"token" : token},{'$set': { "name" : name, "contact": contact}})
        updated_data = user.find_one({"token": token}, {"name": name, "contact": contact ,"_id":0})
        return jsonify(updated_data)
        return "DONE"
    except:
        return "Something Went Wrong Try Again Later or Contact Support."

def get_user_detail(token: str, user):
    try:
        token = token.encode('utf-8')
        data = user.find_one({"token": token}, {"name": 1, "email": 1, "contact": 1 ,"_id":0})
        return jsonify(data)
    except Exception as e:
        return "Error!"

def logout_user(token: str, user, deniedToken) -> str:
    token_data = decode_jwt(token)
    try:
        user.update_one({"_id" : token_data},{'$set': { "token" : ""}})
        deniedToken.insert_one({"token": token, "denied_time": str(datetime.now())}).inserted_id
    except:
        return "Some Internal Error Occurred!"
    return jsonify({"msg": "Logout Success!"})
