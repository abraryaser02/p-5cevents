# services/backend/project/__init__.py

import os
from datetime import datetime, timedelta
from random import choice
from lorem_text import lorem
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import hashlib #Added
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

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
    #username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    # Define the relationship with events
    participants = db.relationship('Event', secondary='user_to_event', backref='users')
    def __init__(self, email, password):
        #self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        # Hash the provided password using hashlib and store it in the password_hash field
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        # Compare the provided password with the hashed password stored in the database
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
    
    def get_events(self):
        return self.events
    
    def get_email(self):
        return self.email
    
    def get_userID(self):
        return self.id

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    organization = db.Column(db.String(100), nullable=False)
    contact_information = db.Column(db.Text, nullable=False)
    registration_link = db.Column(db.String(128), nullable=False)
    keywords = db.Column(JSON, nullable=False)

    # Define the relationship with users
    participants = db.relationship('User', secondary='user_to_event', backref='events')
    def __init__(self, name, description, location, start_time, end_time, organization, contact_information, registration_link, keywords):
        self.name = name
        self.description = description
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.organization = organization
        self.contact_information = contact_information
        self.registration_link = registration_link
        self.keywords = keywords

    def get_eventId(self):
        return self.id

class User_To_Event(db.Model):
    __tablename__ = "user_to_event"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


# Create a scheduler instance
scheduler = BackgroundScheduler()
scheduler.start()

# delete expired events
def delete_expired_events():
    current_time = datetime.now()
    expired_events = Event.query.filter(Event.end_time < current_time).all()
    for event in expired_events:
        db.session.delete(event)
    db.session.commit()

# Runs every hour to check for expired events
scheduler.add_job(
    func=delete_expired_events,
    trigger=IntervalTrigger(hours=1)
)


#----------user routes-----------

@app.route('/login', methods=['POST'])
def login():
    # Assuming the client sends username and password in JSON format
    login_data = request.json

    # Check if the received data contains username and password
    if 'email' in login_data and 'password' in login_data:
        # Extract username and password from the request data
        email = login_data['email']
        password = login_data['password']
        
        # Query the database to find the user by username
        user = User.query.filter_by(email=email).first()
        
        # Validate the credentials
        if user and user.check_password(password):
            # Return success response
            return jsonify({'success': True, 'message': 'Login successful', 'userId': user.get_userID(), 'email': user.get_email()})
        else:
            # Return failure response for invalid credentials
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    else:
        # Return failure response if username or password is missing
 
        return jsonify({'success': False, 'message': 'Username or password missing'}), 400
'''
curl -X POST http://localhost:5001/login \
     -H "Content-Type: application/json" \
     -d '{"email": "example@example.com", "password": "securepassword"}'
''' 
# Route for creating a new user
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()

    #username = data['username']
    email = data['email']
    password = data['password']

    # Check if both user ID and event ID are provided
    if email is None or password is None:
        return jsonify({'message': 'email or password missing'}), 400
    
    # Check if the email already exists in the database
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email already exists'}), 409  # 409 Conflict
    
    # Create a new user instance
    new_user = User(email=email, password=password)

    try:
        # Add the new user to the database session and commit changes
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        # Rollback changes if an error occurs
        db.session.rollback()
        return jsonify({'message': 'Failed to create user', 'details': str(e)}), 500
   
'''
curl -X POST http://localhost:5001/create_user \
     -H "Content-Type: application/json" \
     -d '{"email": "example@example.com", "password": "securepassword"}'
''' 
@app.route('/add_event_to_user', methods=['POST'])
def add_event_to_user():
    # Assuming the client sends JSON data containing the user ID and event ID
    data = request.json

    # Extract user ID and event ID from the request data
    user_id = data.get('user_id')
    event_id = data.get('event_id')

    # Check if both user ID and event ID are provided
    if user_id is None or event_id is None:
        return jsonify({'message': 'User ID or event ID missing'}), 400

    # Query the user and event objects from the database
    user = User.query.get(user_id)
    event = Event.query.get(event_id)

    # Check if both user and event exist
    if user is None or event is None:
        return jsonify({'message': 'User or event not found'}), 404

    # Add the event to the user's list of events
    user.events.append(event)

    try:
        # Commit the changes to the database
        db.session.commit()
        return jsonify({'message': 'Event added to user successfully'}), 201
    except Exception as e:
        # Rollback changes if an error occurs
        db.session.rollback()
        return jsonify({'message': 'Failed to add event to user', 'details': str(e)}), 500

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
                'email': user.email,
                'password': user.password_hash,
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
        'password': user.password_hash,
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

    new_user = User (email=email, password = password)

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
            'registration_link': event.registration_link,
            'keywords': event.keywords
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
            'contact_information': event.contact_information,
            'registration_link': event.registration_link,
            'keywords': event.keywords
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

# get event key words
@app.route('/get_event/<int:event_id>/keywords', methods=['GET'])
def get_event_keywords(event_id):
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({'keywords': event.keywords})

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
    keywords = data['keywords']


    new_event = Event(name=name, description=description, location=location, start_time=start_time, end_time=end_time, organization=organization, contact_information=contact_information,registration_link=registration_link, keywords=keywords)

    try:
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'message': 'Event created successfully', 'eventID': new_event.get_eventId()}), 200
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
  "end_time": "2024-03-22T15:30:00",
  "organization": "Event Organization",
  "contact_information": "contact info",
  "registration_link": "registration link",
  "keywords": ["keyword1", "keyword2", "keyword3"]
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
    keywords = ["keyword1", "keyword2", "keyword3"]

    new_event = Event(name=name, description=description, location=location, start_time=start_time, end_time = end_time, organization=organization, contact_information=contact_information, registration_link=registration_link, keywords=keywords)

    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Test events created successfully'})


if __name__ == '__main__':
    socketio.run(app, debug=True)

#--------------user to event routes--------------
#Get all liked events by user_id
@app.route('/events_by_user/<int:user_id>', methods = ['GET'])
def events_by_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    events = user.get_events()
    
    events_list = [{
        'id': event.id,
        'name': event.name,
        'description': event.description,
        'location': event.location,
        'start_time': event.start_time.isoformat(),
        'end_time': event.end_time.isoformat(),
        'organization': event.organization,
        'contact_information': event.contact_information,
        'registration_link': event.registration_link,
    } for event in events]

    return jsonify(events_list)

'''
curl -X GET http://localhost:5001/events_by_user/1
'''
#Add a new row in the database
@app.route('/toggle_user_event', methods=['POST'])
def toggle_user_event():
    data = request.get_json()
    user_id = data.get('user_id')
    event_id = data.get('event_id')

    if not user_id or not event_id:
        return jsonify({'error': 'Missing user_id or event_id'}), 400

    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if event exists
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    # Check for existing association
    existing_association = User_To_Event.query.filter_by(user_id=user_id, event_id=event_id).first()
    if existing_association:
        # If found, delete it
        db.session.delete(existing_association)
        db.session.commit()
        return jsonify({'message': 'User removed from event successfully'}), 200

    # If not found, create new association
    new_association = User_To_Event(user_id=user_id, event_id=event_id)
    db.session.add(new_association)
    db.session.commit()
    return jsonify({'message': 'User added to event successfully'}), 201

'''
curl -X POST http://localhost:5001/toggle_user_event \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "event_id": 1}'
''' 