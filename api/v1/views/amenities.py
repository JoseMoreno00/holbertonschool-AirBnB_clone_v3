#!/usr/bin/python3
"""
new view for amenities objects that handles RESTFul API actions
"""
from models import storage
from models.amenity import Amenity
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/amenities", methods=["GET"],
                 strict_slashes=False)
def getAmenity():
    """Retrieves the list of all Amenity objects"""
    all_amenities = []
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def getAmenityID(amenity_id):
    """Retrieves a Amenity object: """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def createAmenity():
    """Creates a Amenity"""
    amenity = request.get_json()
    if request.is_json:
        if "name" not in amenity:
            return "Missing name", 400
        objNew = Amenity(**amenity)
        storage.new(objNew)
        storage.save()
        return jsonify(objNew.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def updateAmenity(amenity_id):
    """Updates a Amenity object"""
    amenities = storage.get(Amenity, amenity_id)
    gitignore = ["id", "created_at", "updated_at", "state_id"]
    try:
        data = request.get_json()
        for k, v in data.items():
            if k not in gitignore:
                setattr(amenities, k, v)
        storage.save()
        return jsonify(amenities.to_dict()), 200
    except Exception:
        if amenities is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
