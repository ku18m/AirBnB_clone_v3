#!/usr/bin/python3
"""app_views blueprint amenities handler module"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route(
    '/cities/<city_id>/places',
    methods=['GET', 'POST'],
    strict_slashes=False
    )
def handle_places(city_id):
    """handle places based on request method"""
    from models import storage
    city = storage.get("City", city_id)
    if city is None:
        from api.v1.app import not_found
        return not_found(None)
    if request.method == 'GET':
        return jsonify(
            [place.to_dict() for place in city.places]
            )
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        if "user_id" not in data:
            return jsonify({"error": "Missing user_id"}), 400
        if storage.get("User", data["user_id"]) is None:
            from api.v1.app import not_found
            return not_found(None)
        if "name" not in data:
            return jsonify({"error": "Missing name"}), 400
        from models.place import Place
        place = Place(**data)
        place.city_id = city_id
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route(
    '/places/<place_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False
    )
def handle_place(place_id):
    """handle a specific place based on request method"""
    from models import storage
    place = storage.get("Place", place_id)
    if place is None:
        from api.v1.app import not_found
        return not_found(None)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id',
                           'user_id',
                           'city_id',
                           'created_at',
                           'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route(
    '/places_search',
    methods=['POST'],
    strict_slashes=False
    )
def handle_places_search():
    """handle places search"""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    from models import storage
    all_places = storage.all("Place").values()
    places = []
    if "states" in data:
        for state_id in data["states"]:
            state = storage.get("State", state_id)
            if state is not None:
                for city in state.cities:
                    places.extend(city.places)
    if "cities" in data:
        for city_id in data["cities"]:
            city = storage.get("City", city_id)
            if city is not None:
                places.extend(city.places)
    if "amenities" in data:
        amenities = [storage.get("Amenity", amenity_id)
                     for amenity_id in data["amenities"]]
        for place in all_places:
            if all(amenity in place.amenities for amenity in amenities):
                places.append(place)
    places = list(set(places))
    return jsonify([place.to_dict() for place in places])
