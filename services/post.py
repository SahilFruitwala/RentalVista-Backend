from services.token import decode_jwt
from bson.objectid import ObjectId
from json import dumps

def add_post(token: str, data, rooms) -> str:
    token_data = decode_jwt(token)
    images = []
    for item in data['images']:
        images.append(item['dataURL'])
    print(data['headline'])
    try:
        rooms.insert({"userID" : ObjectId(token_data), "images": images, "title": data['headline'], "ratings": 4, "reviews": [], "description": data['detail'], "rent": data['rent'], "isPromoted": "false", "isPetAllowed": data['petFriendly'], "isFurnished": data['furnishing'], "Amenities": data['amenities'], "Location": data['location'], "Availability": data['date'], "Bedrooms": data['bedrooms'], "Bathrooms": data['bathrooms']})
        # rooms.insert({userID : ObjectId(token_data)})

        # if user.count_documents({"email": email}) == 0:
        #     hashed_password = bcrypt.generate_password_hash(password)
        #     user_id = user.insert_one({"name":name, "email": email, "password": hashed_password, "contact": contact, "token": ""}).inserted_id
        #     return dumps({"msg" : 'Registration Success!'}) , 200

        return dumps({"msg" : "Post added successfully!"}) , 200
    except Exception as e:
        print(str(e))
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500

def get_rooms(token: str, rooms) -> str:
    print("fetching")
    token_data = decode_jwt(token)
    try:
        data = rooms.find({"userID" : ObjectId(token_data)})
        print("data is: "+dumps(data))
        return dumps(data), 200
        # rooms.insert({"userID" : ObjectId(token_data), "images": images, "title": data['headline'], "ratings": 4, "reviews": [], "description": data['detail'], "rent": data['rent'], "isPromoted": "false", "isPetAllowed": data['petFriendly'], "isFurnished": data['furnishing'], "Amenities": data['amenities'], "Location": data['location'], "Availability": data['date'], "Bedrooms": data['bedrooms'], "Bathrooms": data['bathrooms']})
        # rooms.insert({userID : ObjectId(token_data)})

        # if user.count_documents({"email": email}) == 0:
        #     hashed_password = bcrypt.generate_password_hash(password)
        #     user_id = user.insert_one({"name":name, "email": email, "password": hashed_password, "contact": contact, "token": ""}).inserted_id
        #     return dumps({"msg" : 'Registration Success!'}) , 200

        # return dumps({"msg" : "Post added successfully!"}) , 200
    except Exception as e:
        print(str(e))
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500