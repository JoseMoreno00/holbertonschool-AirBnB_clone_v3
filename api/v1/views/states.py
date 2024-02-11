#!/usr/bin/python3
"""new view for State objects that handles all default RESTFul API actions"""
from models import storage
from models.state import State
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
import os


app = Flask(__name__)


@app_views.route("/states/", methods=["GET"], strict_slashes=False)
def getStates():
    """Retrieves the list of all State objects"""
    all_states = []
    states = storage.all(State)
    for objs in states:
        all_states.append(states[objs].to_dict())
    return jsonify(all_states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def getStatesID(state_id):
    """Retrieves a State object: """
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    return jsonify(states.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteStates(state_id):
    """Deletes a State object"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    storage.delete(states)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def createStates():
    """Creates a State"""
    if request.is_json:
        data = request.get_json()
        if "name" not in data:
            return "Missing name", 400
        objNew = State(**data)
        storage.new(objNew)
        storage.save()
        return jsonify(objNew.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def updateState(state_id):
    """Updates a State object"""
    states = storage.get(State, state_id)
    gitignore = ["id", "created_at", "updated_at"]
    try:
        data = request.get_json()
        for k, v in data.items():
            if k not in gitignore:
                setattr(states, k, v)
        storage.save()
        return jsonify(states.to_dict()), 200
    except Exception:
        if states is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
