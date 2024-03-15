#!/usr/bin/env python3
"""
Contains Order class
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base


class Order(BaseModel, Base):
    """ Order class
    """
    __tablename__ = "orders"
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    recipient_name = Column(String(250), nullable=False)
    recipient_address = Column(String(250), nullable=False)
    message = Column(String(250), nullable=True)
    products = relationship(
        "Product",
        backref="order",
        cascade="all, delete-orphan")
