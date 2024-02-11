#!/usr/bin/python3
"""New view for User objects that handles RESTFul API actions."""
from models import storage
from models.user import User
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/users", methods=["GET"],
                 strict_slashes=False)
def getUser():
    """Retrieves the list of all Users objects"""
    all_users = []
    users = storage.all(User)
    for amenity in users.values():
        all_users.append(amenity.to_dict())
    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def getUserID(user_id):
    """Retrieves a User object: """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteUser(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def createUser():
    """Creates a User"""
    user = request.get_json()
    if request.is_json:
        if 'email' not in user:
            return "Misiing email", 400
        if 'password' not in user:
            return "Missing password", 400
        objNew = User(**user)
        storage.new(objNew)
        storage.save()
        return jsonify(objNew.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def updateUser(user_id):
    """Updates a User object"""
    users = storage.get(User, user_id)
    gitignore = ["id", "created_at", "updated_at", "state_id"]
    try:
        data = request.get_json()
        for k, v in data.items():
            if k not in gitignore:
                setattr(users, k, v)
        storage.save()
        return jsonify(users.to_dict()), 200
    except Exception:
        if users is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
