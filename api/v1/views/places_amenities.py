#!/usr/bin/python3
"""app_views blueprint amenities handler module"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route(
    '/places/<place_id>/amenities',
    methods=['GET'],
    strict_slashes=False
    )
def handle_place_amenities(place_id):
    """handle amenities of a place"""
    from models import storage
    place = storage.get("Place", place_id)
    if place is None:
        from api.v1.app import not_found
        return not_found(None)
    return jsonify(
        [amenity.to_dict() for amenity in place.amenities]
        )


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE', 'POST'],
    strict_slashes=False
    )
def handle_place_amenity(place_id, amenity_id):
    """handle a specific amenity of a place"""
    from models import storage, storage_t
    place = storage.get("Place", place_id)
    if place is None:
        from api.v1.app import not_found
        return not_found(None)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        return not_found(None)
    if request.method == 'DELETE':
        if amenity not in place.amenities:
            return not_found(None)
        if storage_t == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.remove(amenity)
        place.save()
        return jsonify({}), 200
    if request.method == 'POST':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        if storage_t == 'db':
            place.amenities.append(amenity)
        else:
            place.amenity_ids.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
