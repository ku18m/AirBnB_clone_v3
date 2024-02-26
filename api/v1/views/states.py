#!/usr/bin/python3
"""app_views blueprint states handler module"""
from api.v1.views import app_views
from flask import jsonify, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Return all states"""
    from models import storage
    return jsonify(
        [state.to_dict() for state in storage.all("State").values()]
        )


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Return a state"""
    from models import storage
    state = storage.get("State", state_id)
    if state is None:
        from api.v1.app import not_found
        return not_found(None)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False
    )
def delete_state(state_id):
    """Return a state"""
    from models import storage
    state = storage.get("State", state_id)
    if state is None:
        from api.v1.app import not_found
        return not_found(None)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Return a state"""
    from models import storage
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    from models.state import State
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Return a state"""
    from models import storage
    state = storage.get("State", state_id)
    if state is None:
        from api.v1.app import not_found
        return not_found(None)
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
