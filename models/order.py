#!/usr/bin/python3
"""
Product model
"""
from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

order_product_association = Table(
    "order_product_association",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("product_id", Integer, ForeignKey("products.id"))
)


class Order(BaseModel, Base):
    """ Product class
    """
    __tablename__ = "orders"
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    recipient_name = Column(String(250), nullable=False)
    recipient_address = Column(String(250), nullable=False)
    message = Column(String(250), nullable=True)
    products = relationship('Product',
                            secondary=order_product_association,
                            backref='orders')
    payment_method_type = Column(String(250), nullable=True)
    amount = Column(Integer, nullable=True)
    currency = Column(String(250), nullable=True)
    status = Column(String(250), default="Pending", nullable=True)
    charge_id = Column(String(250), nullable=False)
