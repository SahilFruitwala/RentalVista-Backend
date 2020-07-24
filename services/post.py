from services.token import decode_jwt
from bson.objectid import ObjectId
from json import dumps, loads

def delete_room(roomID, rooms) -> str:
    try:
        print(type(roomID))
        res = rooms.delete_one({"_id": ObjectId(loads(roomID))})
        return dumps({"msg" : "Post deleted successfully!"}) , 200
    except Exception as e:
        print(str(e))
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500

def add_post(token: str, data, rooms) -> str:
    token_data = decode_jwt(token)
    images = []
    for item in data['images']:
        images.append(item['dataURL'])
    print(data['headline'])
    try:
        rooms.insert({"userID" : ObjectId(token_data), "images": images, "title": data['headline'], "ratings": 4, "reviews": [], "description": data['detail'], "rent": data['rent'], "isPromoted": "false", "isPetAllowed": data['petFriendly'], "isFurnished": data['furnishing'], "Amenities": data['amenities'], "Location": data['location'], "Availability": data['date'], "Bedrooms": data['bedrooms'], "Bathrooms": data['bathrooms']})
        return dumps({"msg" : "Post added successfully!"}) , 200
    except Exception as e:
        print(str(e))
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500

def get_rooms(token: str, rooms) -> str:
    print("fetching")
    token_data = decode_jwt(token)
    rooms_list = []
    try:
        data = rooms.find({"userID" : ObjectId(token_data)})
        for room in data:
            roomID = dumps(room['_id'],default=str)
            userID = dumps(room['userID'],default=str)
            description = room['description']
            image = room['images'][0]
            rating = room['ratings']
            isPromoted = room['isPromoted']
            rent = room['rent']
            dict_room = {
                'roomID':roomID,
                'userID':userID,
                'image': image,
                'rating': rating,
                'isPromoted':isPromoted,
                'rent': rent,
                'description': description
            }
            rooms_list.append(dict_room)
        return dumps(rooms_list), 200
    except Exception as e:
        print(str(e))
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500