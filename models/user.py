#!/usr/bin/env python3
"""
Contains User class
"""
from sqlalchemy import Column, String
from models.basemodel import BaseModel, Base


class User(BaseModel, Base):
    """ User class
    """
    __tablename__ = "users"
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
