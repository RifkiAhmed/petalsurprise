#!/usr/bin/python3
""" Route module for the API
"""
from flask import Flask, request, abort, redirect, url_for, render_template
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
        abort(401)


@app.errorhandler(403)
def forbidden(_):
    """ Redirect user to the home page for 403 Forbidden error
    """
    return redirect(url_for('views.index'))


@app.errorhandler(404)
def not_found(_):
    """ Returns a custom template for 404 Not found error
    """
    return render_template('404.html')


@app.teardown_appcontext
def teardown(_):
    storage.close()


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
