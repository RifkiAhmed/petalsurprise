#!/usr/bin/env python3
"""
Initializes the authentication object and database session for the APP
"""

from models.engine.db import DB


storage = DB()
storage._session

AUTH = None
if storage:
    from models.auth import Auth
    AUTH = Auth()

