#!/usr/bin/python3
"""new view for cities objects that handles all default RESTFul API actions"""
from models import storage
from models.state import State, City
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def getCity(state_id):
    """Retrieves the list of all City objects"""
    all_cities = []
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    for cities in states.cities:
        all_cities.append(cities.to_dict())
    return jsonify(all_cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def getCityID(city_id):
    """Retrieves a City object: """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteCity(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def createCity(state_id):
    """Creates a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
        if "name" not in data:
            return "Missing name", 400
        data["state_id"] = state_id
        objNew = City(**data)
        storage.new(objNew)
        storage.save()
        return jsonify(objNew.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def updateCity(city_id):
    """Updates a State object"""
    city = storage.get(City, city_id)
    gitignore = ["id", "created_at", "updated_at", "state_id"]
    try:
        data = request.get_json()
        for k, v in data.items():
            if k not in gitignore:
                setattr(city, k, v)
        storage.save()
        return jsonify(city.to_dict()), 200
    except Exception:
        if city is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
