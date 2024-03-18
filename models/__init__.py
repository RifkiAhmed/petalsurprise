#!/usr/bin/env python3
"""
Initializes the authentication and database session for the APP
"""
from models.auth import Auth
from models.engine.db import DB

AUTH = Auth()
storage = DB()
storage._session
