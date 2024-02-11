#!/usr/bin/python3
"""Module of the App"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """Method to call storage.close()"""
    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    """Method that errorhandler for 404 error oage not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST", "0.0.0.0"),
            port=os.getenv("HBNB_API_PORT", "5000"),
            threaded=True, debug=False)
