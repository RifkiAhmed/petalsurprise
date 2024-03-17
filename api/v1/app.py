#!/usr/bin/python3
""" Route module for the API
"""
from flask import Flask
from api.v1.views import views
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(views)


@app.teardown_appcontext
def teardown(_):
    """
    Closes the SQLAlchemy session after each request.
    """
    storage.close()


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
