#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """ BaseModel class
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the object"""
        exclude_attrs = ['_sa_instance_state']
        dic = {"__class__": self.__class__.__name__}
        for key, value in self.__dict__.items():
            if key not in exclude_attrs:
                dic[key] = value
        return dic
