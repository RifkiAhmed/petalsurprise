#!/usr/bin/python3
""" Route module for the API
"""
from flask import Flask, request, jsonify, abort, redirect, url_for
from flask_cors import CORS
from api.v1.views import views
from models import storage, AUTH
from os import getenv

app = Flask(__name__)
app.register_blueprint(views)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.before_request
async def before_request():
    """ Filter each request to ensure authentication
    """
    if AUTH.require_auth(request):
        abort(403)


@app.errorhandler(401)
@app.errorhandler(403)
def unauthorized(error) -> str:
    """ Redirect user to the home page for Unauthorized and Forbidden access
    """
    return redirect(url_for('views.index'))


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(exception=None):
    storage.close()


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
