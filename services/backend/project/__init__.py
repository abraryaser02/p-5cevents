# services/backend/project/__init__.py

import os
from datetime import datetime, timedelta
from random import choice
from lorem_text import lorem
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO, emit

# instantiate the app
app = Flask(__name__)
CORS(app)


socketio = SocketIO(app, cors_allowed_origins="*")


# set configuration
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


# instantiate the database
db = SQLAlchemy(app)


# models 
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    organization = db.Column(db.String(100), nullable=False)

    def __init__(self, name, description, location, time, organization):
        self.name = name
        self.description = description
        self.location = location
        self.time = time
        self.organization = organization


# routes
@app.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@app.route('/users', methods=['GET'])
def get_users():
    try:
        # Query all users from the database
        users = User.query.all()
        # Convert each user into a dictionary
        users_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'active': user.active
            }
            users_list.append(user_data)
        # Return a JSON response containing the list of user dictionaries
        return jsonify(users_list)
    except e:
        return jsonify({'message': 'error retrieving users'})


# route for retrieving all events
@app.route('/all_events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = []
    for event in events:
        event_data = {
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'location': event.location,
            'time': event.time,
            'organization': event.organization
        }
        events_list.append(event_data)
    return jsonify(events_list)

# get event by id
@app.route('/get_event/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    event_data = {
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'location': event.location,
            'time': event.time,
            'organization': event.organization
        }
    return jsonify(event_data)

# get event name
@app.route('/get_event/<int:event_id>/name', methods=['GET'])
def get_event_name(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({'name': event.name})

# get event description
@app.route('/get_event/<int:event_id>/description', methods=['GET'])
def get_event_description(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({'description': event.description})

# get event location
@app.route('/get_event/<int:event_id>/location', methods=['GET'])
def get_event_location(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({'location': event.location})

# get event time
@app.route('/get_event/<int:event_id>/time', methods=['GET'])
def get_event_time(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({'time': event.time})

# get event organization
@app.route('/get_event/<int:event_id>/organization', methods=['GET'])
def get_event_organization(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({'organization': event.organization})

# route for creating a new event
@app.route('/create_event', methods=['POST'])
def create_event():
    data = request.get_json()

    name = data['name']
    description = data['description']
    location = data['location']
    time = data['date']
    organization = data['organization']

    new_event = Event(name=name, description=description, location=location, time=time, organization=organization)

    try:
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'message': 'Event created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create event', 'details': str(e)}), 500

'''
curl -X POST http://localhost:5001/create_event \
-H "Content-Type: application/json" \
-d '{
  "name": "Event Name",
  "description": "Event Description",
  "location": "Event location",
  "time": "2024-03-22T15:30:00",
  "organization": "Event Organization"
}'
'''

# route for deleting an event
@app.route('/delete_event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404

    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete event', 'details': str(e)}), 500

# curl -X DELETE http://localhost:5002/events/<id>
    

# generate a test event
@app.route('/test_event', methods=['GET'])
def geneate_events():
    organizations = ['Pomona College', 'CMC', 'Scripps', 'HMC', 'Pitzer College']

    name = lorem.words(3)
    description = lorem.words(10)
    location = lorem.words(2)
    time = datetime.now() + timedelta(days=choice(range(1, 30)))
    organization = choice(organizations)

    new_event = Event(name=name, description=description, location=location, time=time, organization=organization)

    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Test events created successfully'})


if __name__ == '__main__':
    socketio.run(app, debug=True)