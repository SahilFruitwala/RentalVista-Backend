from flask import flash, jsonify
from datetime import datetime
import json

def get_all_property_images(properties):
    try:
        listofRoomsImages = []
        for room in properties.find({}):
            image = room['images'][0]
            dict_room = {
                'image': image,
            }
            listofRoomsImages.append(dict_room)
        print(listofRoomsImages)
        return jsonify({"Data":listofRoomsImages,"Status":"Success"})
    except Exception as e:
        return jsonify({"msg" : 'Some internal error occurred!', "error": str(e)})
