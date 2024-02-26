from models import storage
from flask import Flask
from api.v1.views import app_views
from os import getenv
"""api module main"""


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """Close the database"""
    storage.close()


if __name__ == "__main__":
    """run the app"""
    host = '0.0.0.0' if getenv('HBNB_API_HOST') is None else getenv(
        'HBNB_API_HOST')
    port = 5000 if getenv('HBNB_API_PORT') is None else int(getenv(
        'HBNB_API_PORT'))
    app.run(host=host, port=port, threaded=True)
