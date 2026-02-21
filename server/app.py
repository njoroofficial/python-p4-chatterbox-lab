from flask import Flask, request, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# get all messages
@app.route('/messages', methods=['GET'])
def messages():
    messages = []
    for message in Message.query.all():
        messages.append(message.to_dict())
    
    response =  make_response(
        messages,
        200
    )

    return response

# get message by id
@app.route('/messages/<int:message_id>', methods=['GET'])
def messages_by_id(message_id):
    message = Message.query.filter(Message.id == message_id).first()

    if message:
        body = message.to_dict()
        status = 200
    else:
        body = {'message':f'Message {message_id} not found'}
        status = 404

    return make_response(body, status)

# Create a new message
@app.route("/messages", methods=['POST'])
def create_message():
    new_message = Message(
        body = request.json.get("body"),
        username = request.json.get("username")
        )
    
    db.session.add(new_message)
    db.session.commit()

    return make_response(new_message.to_dict(), 201)

# update a message
@app.route("/messages/<int:message_id>", methods=['PATCH'])
def update_message(message_id):
    message = Message.query.filter(Message.id == message_id).first()

    if message:
        for attr in request.json:
            setattr(message, attr, request.json.get(attr))

        db.session.add(message)
        db.session.commit()

        response = make_response(
            message.to_dict(),
            200
        )
    else:
        response = make_response(
            {"message":"Message not found"},
            404
        )

    return response

# Delete a message
@app.route("/messages/<int:message_id>", methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.filter(Message.id == message_id).first()

    if message:
        db.session.delete(message)
        db.session.commit()

        response_body = {
                "delete_successful": True,
                "message": "Message deleted."
            }
        response = make_response(
                response_body,
                200
            )
    else:
        response = make_response (
            {"Message": "Error deleting the message"},
            404
        )
    
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
