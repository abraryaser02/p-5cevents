# services/events/project/__init__.py


import os
import datetime
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

    def __init__(self, name):
        self.name = name

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
            'name': event.name
        }
        events_list.append(event_data)
    return jsonify(events_list)

# route for creating a new event
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Missing name parameter'}), 400

    name = data['name']
    new_event = Event(name=name)

    try:
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'message': 'Event created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create event', 'details': str(e)}), 500

# curl -X POST \ -H "Content-Type: application/json" \ -d "{\"name\": \"Your Event Name\"}" \ http://localhost:5002/events

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