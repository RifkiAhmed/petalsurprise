#!/usr/bin/env python3
"""
Product model
"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Integer, Boolean


class Product(BaseModel, Base):
    """ Product class
    """
    __tablename__ = "products"
    name = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(250), nullable=True)
    img_path = Column(String(250), nullable=False)
    listed = Column(Boolean, default=True)
