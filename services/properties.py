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
            isPromoted = room['isPromoted']
            isPetAllowed = room['isPetAllowed']
            rent = room['rent']
            dict_room = {
                'roomID':roomID,
                'userID':userID,
                'image': image,
                'rating': rating,
                'isPromoted':isPromoted,
                'rent': rent,
                'description': description,
                'isPetAllowed': isPetAllowed
            }
            listofRooms.append(dict_room)
        print(listofRooms)
        return jsonify({"Data":listofRooms,"Status":"Success"})
    except Exception as e:
        return jsonify({"msg" : 'Some internal error occurred!', "error": str(e)})
