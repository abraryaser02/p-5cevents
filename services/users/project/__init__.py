# services/users/project/__init__.py


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
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email


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
