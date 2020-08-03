from flask import flash, jsonify
from datetime import datetime
import json

def get_all_properties(properties):
    try:
        listofRooms = []
        for room in properties.find({}):
            roomID = json.dumps(room['_id'],default=str)
            userID = json.dumps(room['userID'],default=str)
            description = room['description']
            image = room['images'][0]
            rating = room['ratings']
            disabled = room['disabled']
            isPromoted = room['isPromoted']
            isPetAllowed = room['isPetAllowed']
            rent = room['rent']
            date = room['Availability']
            bedrooms = room['Bedrooms']
            bathrooms = room['Bathrooms']
            dict_room = {
                'roomID':roomID,
                'userID':userID,
                'image': image,
                'rating': rating,
                'isPromoted':isPromoted,
                'rent': rent,
                'disabled': disabled,
                'description': description,
                'isPetAllowed': isPetAllowed,
                'date': date,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms
            }
            listofRooms.append(dict_room)
        #print(listofRooms)
        return jsonify({"Data":listofRooms,"Status":"Success"})
    except Exception as e:
        return jsonify({"msg" : 'Some internal error occurred!', "error": str(e)})
