#!/usr/bin/python3
"""new view for places objects that handles all default RESTFul API actions"""
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def getPlace(city_id):
    """Retrieves the list of all Places objects"""
    all_places = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def getPlaceID(place_id):
    """Retrieves a City object: """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def deletePlace(place_id):
    """Deletes a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def createPlace(city_id):
    """Creates a State"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
        if "user_id" not in data:
            return "Missing user_id", 400
        if "name" not in data:
            return "Misiing name", 400
        if storage.get(User, data["user_id"]) is None:
            abort(404)
        objNew = Place(city_id=city_id, **data)
        storage.new(objNew)
        storage.save()
        return jsonify(objNew.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("places/<place_id>", methods=["PUT"], strict_slashes=False)
def updatePlace(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    gitignore = ["id", "city_id", "created_at", "updated_at", "user_id"]
    try:
        data = request.get_json()
        for k, v in data.items():
            if k not in gitignore:
                setattr(place, k, v)
        storage.save()
        return jsonify(place.to_dict()), 200
    except Exception:
        if place is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
