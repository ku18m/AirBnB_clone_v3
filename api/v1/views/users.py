#!/usr/bin/python3
"""app_views blueprint users handler module"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route(
    '/users',
    methods=['GET', 'POST'],
    strict_slashes=False
    )
def handle_users():
    """handle users based on request method"""
    from models import storage
    if request.method == 'GET':
        return jsonify(
            [user.to_dict() for user in storage.all("User").values()]
            )
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        if "email" not in data:
            return jsonify({"error": "Missing email"}), 400
        if "password" not in data:
            return jsonify({"error": "Missing password"}), 400
        from models.user import User
        user = User(**data)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route(
    '/users/<user_id>',
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False
    )
def handle_user(user_id):
    """handle a specific user based on request method"""
    from models import storage
    user = storage.get("User", user_id)
    if user is None:
        from api.v1.app import not_found
        return not_found(None)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
