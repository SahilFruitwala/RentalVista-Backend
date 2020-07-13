from .token import encode_jwt, decode_jwt

def register_user(name: str, email: str, password: str, contact:str, user, bcrypt) -> str:
    if user.count_documents({"email": email}) == 0:
        hashed_password = bcrypt.generate_password_hash(password)
        return str(user.insert_one({"name":name, "email": email, "password": hashed_password, "contact": contact}).inserted_id)
    return "User Already Exist!"

def validate_user(email: str, password: str, user, bcrypt) -> str:
    
    if user.count_documents({"email": email}) == 0:
        return "User does not exist!"
    
    result = user.find_one({"email":email}, {"password": password, "_id":1})
    if bcrypt.check_password_hash(result['password'], password):
        print(type(result['_id']))
        token = encode_jwt(str(result['_id'])) # converted id into string then passed to encode_jwt
        return {'msg': 'Login Success!', "token": token.decode('utf-8')} # need to decode JWT from bytes to string 
    return "Email or Password is incorrect!"

