#!/usr/bin/python3
"""Blueprint for API 
"""
from flask import Blueprint

views = Blueprint('views', __name__)

from api.v1.views.index import *
from api.v1.views.user import *
