from .token import encode_jwt, decode_jwt
from flask import flash
from json import dumps
from flask_mail import Message
from .password_generator import generate_random_pass
from datetime import datetime
from bson.objectid import ObjectId

def book_appointment(adata, appointment):
    date = adata['date'] + 'Aug'
    print(adata)
    try:
        appointment.insert_one({"postid" : adata['postid'], "date": date, "time": adata["time"], "email" : adata['email'], "owneremail": adata['owneremail'] })
        return dumps({"msg" : 'Appointment Booked'}) , 200
    except Exception as e:
        return dumps({"msg" : 'Some internal error occurred!', "error": str(e)}), 500
    
    