from flask_sqlalchemy import SQLAlchemy
from project import app

# instantiate the database
db = SQLAlchemy(app)

# models 
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    school = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email, password, school):
        self.username = username
        self.email = email
        self.password = password
        self.school = school

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

class User_To_Event(db.Model):
    __talename__ = "user_to_events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)   
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))