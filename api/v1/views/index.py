#!/usr/bin/python3
""" Index module for the API
"""
from flask import render_template
from api.v1.views import views

@views.route('/')
def index():
    """Return index page"""
    return render_template('index.html')
