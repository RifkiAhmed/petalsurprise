#!/usr/bin/python3
""" Route module for the API
"""
from flask import Flask
from api.v1.views import views

app = Flask(__name__)
app.register_blueprint(views)


if __name__ == "__main__":
    app.run('0.0.0.0', 5000, True)
