#!/usr/bin/python3
"""Module index from the app"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats",  strict_slashes=False)
def count():
    """ Count objects """
    dictionaryOBJ = {}
    classes = {
        "Amenity": "amenities",
        "Place": "places",
        "State": "states",
        "City": "cities",
        "Review": "reviews",
        "User": "users"
    }

    for cls in classes:
        count = storage.count(cls)
        dictionaryOBJ[classes.get(cls)] = count
    return jsonify(dictionaryOBJ)
