# services/events/project/__init__.py


import os
import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# instantiate the app
app = Flask(__name__)


# set configuration
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


# instantiate the database
db = SQLAlchemy(app)

# model
class Events(db.Model):
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
