#!/usr/bin/python3
"""
User model
"""
from sqlalchemy import Column, String, Boolean
from models.basemodel import BaseModel, Base


class User(BaseModel, Base):
    """ User class
    """
    __tablename__ = "users"
    email = Column(String(250), nullable=False)
    username = Column(String(250), nullable=True)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    is_admin = Column(Boolean, default=False)
    status = Column(String(250), nullable=True)
