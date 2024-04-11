# services/backend/project/__init__.py

import os
from datetime import datetime, timedelta
from random import choice
from lorem_text import lorem
from flask import Flask, jsonify, request

# instantiate the app
app = Flask(__name__)

# set configuration
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

