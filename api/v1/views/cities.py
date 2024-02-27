#!/usr/bin/python3
"""app_views blueprint cities handler module"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET', 'POST'],
    strict_slashes=False
    )
def handle_cities(state_id):
    """Return all cities"""
    from models import storage
    state = storage.get("State", state_id)
    if state is None:
        from api.v1.app import not_found
        return not_found(None)
    if request.method == 'GET':
        return jsonify(
            [city.to_dict() for city in state.cities]
            )
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in data:
            return jsonify({"error": "Missing name"}), 400
        from models.city import City
        city = City(**data)
        city.state_id = state_id
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route(
    '/cities/<city_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False
    )
def handle_city(city_id):
    """Return a city"""
    from models import storage
    city = storage.get("City", city_id)
    if city is None:
        from api.v1.app import not_found
        return not_found(None)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
