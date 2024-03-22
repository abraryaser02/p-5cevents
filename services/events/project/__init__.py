# services/events/project/__init__.py


import os
from datetime import datetime, timedelta
from random import choice
from lorem_text import lorem
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# instantiate the app
app = Flask(__name__)


# set configuration
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


# instantiate the database
db = SQLAlchemy(app)

# model
class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    organizer = db.Column(db.String(100), nullable=False)

    def __init__(self, name, description, time, organizer):
        self.name = name
        self.description = description
        self.time = time
        self.organizer = organizer

# routes
@app.route('/events/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

# route for retrieving all events
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    events_list = []
    for event in events:
        event_data = {
            'id': event.id,
            'name': event.name,
            'description': event.description,
            'time': event.time,
            'organizer': event.organizer
        }
        events_list.append(event_data)
    return jsonify(events_list)

# route for creating a new event
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()

    name = data['name']
    description = data['description']
    time = data['time']
    organizer = data['organizer']

    new_event = Event(name=name, description=description, time=time, organizer=organizer)

    try:
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'message': 'Event created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create event', 'details': str(e)}), 500

''' 
curl -X POST http://localhost:5002/events \
-H "Content-Type: application/json" \
-d '{
  "name": "Event Name",
  "description": "Event Description",
  "time": "2024-03-22T15:30:00",
  "organizer": "Event Organizer"
}'

'''

# route for deleting an event
@app.route('/events/<int:event_id>', methods=['DELETE'])
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
    

# testing purposes
@app.route('/events/test', methods=['GET'])
def geneate_events():
    organizations = ['Pomona College', 'CMC', 'Scripps', 'HMC', 'Pitzer College']

    name = lorem.words(3)
    description = lorem.words(10)
    time = datetime.now() + timedelta(days=choice(range(1, 30)))
    organizer = choice(organizations)

    new_event = Event(name=name, description=description, time=time, organizer=organizer)

    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Test events created successfully'})


'''
- microservices structure
- one database vs multiple for each service (forein keys )
- structuring directories (ie. routes, models, )
- should we use flask blueprints (modularity/reusability) vs multiple flask apps in docker

'''