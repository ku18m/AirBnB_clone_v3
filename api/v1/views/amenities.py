#!/usr/bin/python3
"""app_views blueprint amenities handler module"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route(
    '/amenities',
    methods=['GET', 'POST'],
    strict_slashes=False
    )
def handle_amenities():
    """handle amenities based on request method"""
    from models import storage
    if request.method == 'GET':
        return jsonify(
            [amenity.to_dict() for amenity in storage.all("Amenity").values()]
            )
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in data:
            return jsonify({"error": "Missing name"}), 400
        from models.amenity import Amenity
        amenity = Amenity(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False
    )
def handle_amenity(amenity_id):
    """handle a specific amenity based on request method"""
    from models import storage
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        from api.v1.app import not_found
        return not_found(None)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
