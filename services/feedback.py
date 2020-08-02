from flask import flash
from json import dumps
from flask_mail import Message
from datetime import datetime


def submit_feedback(email: str, body: str, feedback, mail):
    try:
        feedback_id = feedback.insert_one({"email": email, "body": body, "feedback_time": str(datetime.now())}).inserted_id
    except Exception as e:
        return dumps({"msg": 'Some internal error occurred!', "error": str(e)}), 500
    else:
        try:
            msg=Message('Feedback Received', recipients=[email])
            msg.html=('<h2>We appreciate your feedback!</h2>'
                        '<p>Reference No. of your feedback is <b>' +
                            str(feedback_id)+'</b></p>'
                        '<p>Thank You</P>'
                        '<p>RentalVista Team</P>')
            mail.send(msg)
            flash(f'Feedback confirmation sent to {email}.')
            return dumps({"msg": "Feedback Received!"}), 200
        except Exception as e:
            return dumps({"msg": 'Some internal error occurred!', "error": str(e)}), 500
