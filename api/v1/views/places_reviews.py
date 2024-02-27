#!/usr/bin/python3
"""app_views blueprint amenities handler module"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['GET', 'POST'],
    strict_slashes=False
    )
def handle_reviews(place_id):
    """handle reviews based on request method"""
    from models import storage
    place = storage.get("Place", place_id)
    if place is None:
        from api.v1.app import not_found
        return not_found(None)
    if request.method == 'GET':
        return jsonify(
            [review.to_dict() for review in place.reviews]
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
        if "text" not in data:
            return jsonify({"error": "Missing text"}), 400
        from models.review import Review
        review = Review(**data)
        review.place_id = place_id
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route(
    '/reviews/<review_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False
    )
def handle_review(review_id):
    """handle a specific review based on request method"""
    from models import storage
    review = storage.get("Review", review_id)
    if review is None:
        from api.v1.app import not_found
        return not_found(None)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id',
                           'user_id',
                           'place_id',
                           'created_at',
                           'updated_at']:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
