#!/usr/bin/python3
"""New view for places review objects that handles all default
RESTFul API actions"""
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def getPlaceReviews(place_id):
    """Retrieves the list of all Places Reviews objects"""
    places_reviews = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        places_reviews.append(review.to_dict())
    return jsonify(places_reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def getReviewID(review_id):
    """Retrieves a Review object: """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteReviewPlace(review_id):
    """Deletes a place review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def createPlaceReview(place_id):
    """Creates a Place Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.is_json:
        data = request.get_json()
        if "user_id" not in data:
            return "Missing user_id", 400
        if "text" not in data:
            return "Missing text", 400
        if storage.get(User, data["user_id"]) is None:
            abort(404)
        objNew = Review(place_id=place_id, **data)
        storage.new(objNew)
        storage.save()
        return jsonify(objNew.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def updatePlaceReview(review_id):
    """Updates a Place Review object"""
    review = storage.get(Review, review_id)
    gitignore = ["id", "place_id", "created_at", "updated_at", "user_id"]
    try:
        data = request.get_json()
        for k, v in data.items():
            if k not in gitignore:
                setattr(review, k, v)
        storage.save()
        return jsonify(review.to_dict()), 200
    except Exception:
        if review is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
