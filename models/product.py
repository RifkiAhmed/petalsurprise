#!/usr/bin/env python3
"""
Product model
"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Integer


class Product(BaseModel, Base):
    """ Product class
    """
    __tablename__ = "products"
    name = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    img_path = Column(String(250), nullable=False)
