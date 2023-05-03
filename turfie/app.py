import os
from .db import db
from .routes import turfie
from flask import Flask, send_from_directory
from tortoise import run_async

# Initialize the database
run_async(db.init(open('config.json', 'r').read()))


# Create the app
app = Flask(__name__)
# Register the turfie blueprint
app.register_blueprint(turfie)

# register the static files
@app.route('/static/<path:path>')
def get_resource(path):  
    return send_from_directory('static', path)

