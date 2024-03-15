#!/usr/bin/env python3
"""
Contains Product class
"""
from sqlalchemy import Column, Integer, String
from models.basemodel import BaseModel, Base


class Product(BaseModel, Base):
    """ Product class
    """
    __tablename__ = "products"
    name = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    img_path = Column(String(250), nullable=False)
