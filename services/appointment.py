# Author: Krupa Patel - B00828120
from services.token import encode_jwt, decode_jwt
from flask import flash
from json import dumps, loads
from flask_mail import Message
from flask_mail import Mail
from datetime import datetime
from bson.objectid import ObjectId
from flask import json, make_response, jsonify, request, Flask, Response


def book_appointment(token: str, adata, appointment, user, mail):
    date = adata['date'] + ' Aug'
    token_data = decode_jwt(token)
    # userdata = user.find({"_id": ObjectId(token_data)})

    try:
        appointment.insert_one({"userid": ObjectId(token_data), "postid": adata['postid'], "date": date, "time": adata["time"], "email": adata['email'],
                                "owneremail": adata['owneremail']})
        email1 = adata['email']
        email2 = adata['owneremail']
        time = adata['time']
        msg = Message('Appointment Booked', recipients=[email1, email2])
        msg.html = ('<h2>Appointment details</h2>'
                    '<p>Your appointment is booked on <b>'+date+' 2020 on '+time+' PM.</b></p>'
                    '<p><i><b>Note:</b>If you want to cancel or reschedule the appointment please visit our website.</i></P>')
        mail.send(msg)
        return dumps({"msg": 'Appointment Booked'}), 200
    except Exception as e:
        return dumps({"msg": 'Some internal error occurred!', "error": str(e)}), 500


def get_appointments(token: str, appointment, mail):
    token_data = decode_jwt(token)
    appointments_list = []

    appointment_data = appointment.find({"userid": ObjectId(token_data)})
    for i in appointment_data:
        data = {
            'id': dumps(i['_id'], default=str),
            'postid': i['postid'],
            'date': i['date'],
            'time': i['time'],
            'email': i['email'],
            'owneremail': i['owneremail']
        }
        appointments_list.append(data)
        data = {}
    print(appointments_list)
    response = Response(json.dumps(
        appointments_list), status=200, mimetype="application/json")

    return response


def deleteAppointment(roomID, appointment, mail) -> str:
    try:
        res = appointment.delete_one({"_id": ObjectId(loads(roomID))})
        adata = appointment.find_one(
            {"userid": ObjectId(roomID)})
        email1 = adata['email']
        email2 = adata['owneremail']
        time = adata['time']
        date = adata['date'] + ' Aug'
        msg = Message('Appointment Booked', recipients=[email1, email2])
        msg.html = ('<h2>Appointment details</h2>'
                    '<p>Your appointment is cancelled which is on <b>' +
                    date+' 2020 on '+time+' PM.</b></p>'
                    '<p><i><b>Note:</b>If you want to cancel or reschedule the appointment please visit our website.</i></P>')
        mail.send(msg)
        return dumps({"msg": "Appointment deleted successfully!"}), 200
    except Exception as e:
        return dumps({"msg": 'Some internal error occurred while deleting appointment!', "error": str(e)}), 500
