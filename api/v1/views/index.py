#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
"""app_views blueprint index module"""


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status, first endpoint of the api"""
    return jsonify({"status": "OK"})
