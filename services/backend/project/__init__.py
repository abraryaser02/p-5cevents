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
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    # Define the relationship with events
    participants = db.relationship('Event', secondary='user_to_event', backref='users')
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    organization = db.Column(db.String(100), nullable=False)
    contact_information = db.Column(db.Text, nullable=False)
    registration_link = db.Column(db.String(128), nullable=False)

    # Define the relationship with users
    participants = db.relationship('User', secondary='user_to_event', backref='events')
    def __init__(self, name, description, location, start_time, end_time, organization, contact_information, registration_link):
        self.name = name
        self.description = description
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.organization = organization
        self.contact_information = contact_information
        self.registration_link = registration_link

class User_To_Event(db.Model):
    __tablename__ = "user_to_event"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


#----------user routes-----------

@app.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@app.route('/all_users', methods=['GET'])
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
                'password': user.password,
                'active': user.active
            }
            users_list.append(user_data)
        # Return a JSON response containing the list of user dictionaries
        return jsonify(users_list)
    except e:
        return jsonify({'message': 'error retrieving users'})
    
#get user by id
@app.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    user_data = {
        'id': user.id,
        'username': user.username,
        'password': user.password,
        'email': user.email
    }
    return jsonify(user_data)
    
# generate a test user
@app.route('/test_user', methods=['GET'])
def generate_user():
    organizations = ['@pomona.edu', '@cmc.edu', '@scripps.edu', '@hmc.edu', '@pitzer.edu']

    username = lorem.words(1)
    email = lorem.words(1) + choice(organizations)
    password = lorem.words(1)

    new_user = User(username=username, email=email, password = password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Test user created successfully'})


#--------------event routes--------------

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
            'start_time': event.start_time,
            'end_time': event.end_time,
            'organization': event.organization,
            'contact_information': event.contact_information,
            'registration_link': event.registration_link
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
            'start_time': event.start_time,
            'end_time': event.end_time,
            'organization': event.organization,
            'contact_information': event.contact_organization,
            'registration_link': event.registration_link
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

# get event start time
@app.route('/get_event/<int:event_id>/start_time', methods=['GET'])
def get_event_start_time(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({'start_time': event.start_time})

# get event end time
@app.route('/get_event/<int:event_id>/end_time', methods=['GET'])
def get_event_end_time(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({'end_time': event.end_time})

# get event organization
@app.route('/get_event/<int:event_id>/organization', methods=['GET'])
def get_event_organization(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({'organization': event.organization})

# get event contact info
@app.route('/get_event/<int:event_id>/contact_information', methods=['GET'])
def get_event_contact_information(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({'contact_information': event.contact_information})

# get event reg link
@app.route('/get_event/<int:event_id>/registration_link', methods=['GET'])
def get_event_registration_link(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({'registration_link': event.registration_link})

# route for creating a new event
@app.route('/create_event', methods=['POST'])
def create_event():
    data = request.get_json()

    name = data['name']
    description = data['description']
    location = data['location']
    start_time = data['start_time']
    end_time = data['end_time']
    organization = data['organization']
    contact_information = data['contact_information']
    registration_link = data['registration_link']


    new_event = Event(name=name, description=description, location=location, start_time=start_time, end_time=end_time, organization=organization, contact_information=contact_information,registration_link=registration_link)

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
  "start_time": "2024-03-22T15:30:00",
  "end_time": "2024-03-22T15:30:00"
  "organization": "Event Organization"
  "contact_information": "contact info"
  "registration_link": "registration link"
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
def generate_events():
    organizations = ['Pomona College', 'CMC', 'Scripps', 'HMC', 'Pitzer College']

    name = lorem.words(3)
    description = lorem.words(10)
    location = lorem.words(2)
    start_time = datetime.now() + timedelta(days=choice(range(1, 30)))
    end_time = datetime.now() + timedelta(days=choice(range(1, 30)))

    organization = choice(organizations)

    contact_information = lorem.words(3)
    registration_link = lorem.words(1)

    new_event = Event(name=name, description=description, location=location, start_time=start_time, end_time = end_time, organization=organization, contact_information=contact_information, registration_link=registration_link)

    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Test events created successfully'})


if __name__ == '__main__':
    socketio.run(app, debug=True)
