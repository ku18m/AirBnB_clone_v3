#!/usr/bin/python3
"""api module main"""
from models import storage
from flask import Flask
from flask_cors import CORS
from api.v1.views import app_views
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

CORS(app, resources={r"/*": {"origins": host}})


@app.teardown_appcontext
def close_db(error):
    """Close the database"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return a JSON-formatted 404 status code response"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    """
    run the app with the host and port from the environment or default values
    """
    app.run(host=host, port=port, threaded=True)
