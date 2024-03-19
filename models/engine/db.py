#!/usr/bin/python3
"""
DB model
"""
from models.basemodel import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from os import getenv


class DB:
    """ DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                     format(getenv('DB_USER'),
                                            getenv('DB_PWD'),
                                            getenv('DB_HOST'),
                                            getenv('DB_NAME')))
        # Base.metadata.drop_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        Base.metadata.create_all(self._engine)
        if self.__session is None:
            sess_factory = sessionmaker(
                bind=self._engine, expire_on_commit=False)
            DBSession = scoped_session(sess_factory)
            self.__session = DBSession()
        return self.__session

    def all(self, cls):
        """Returns all the object of the given cls argument
        """
        return self._session.query(cls).all()

    def add(self, obj):
        """Add a new object to the database
        """
        if obj:
            self._session.add(obj)
            self._session.commit()
        return None

    def delete(self, obj):
        """Delete the object from the database
        """
        if obj:
            self._session.delete(obj)
            self._session.commit()
        return None

    def save(self):
        """Save change to the database
        """
        if self._session:
            self._session.commit()
        return None

    def get_limit(self, cls, page, per_page):
        """Returns the objects corresponding to the page of size per_page
        """
        start = page * per_page
        end = start + per_page
        products_count = self.count(cls)
        if end > products_count:
            end = products_count
        products = self._session.query(cls).slice(start, end).all()
        return products

    def find_by(self, cls, **kwargs):
        """Returns the first object based on the given keyword argument
        """
        obj = self._session.query(cls).filter_by(**kwargs).first()
        if not obj:
            raise NoResultFound
        return obj

    def find_all(self, cls, **kwargs):
        """Returns all the objects based on the given keyword argument
        """
        objs = self._session.query(cls).filter_by(**kwargs).all()
        if not objs:
            raise NoResultFound
        return objs

    def update(self, obj, **kwargs) -> None:
        """ Updates object attributes with the given key-value pairs
        """
        if obj:
            for key, value in kwargs.items():
                if key in obj.__dict__:
                    setattr(obj, key, value)
                else:
                    raise ValueError
            self._session.commit()
        return None

    def count(self, cls):
        """ Returns the number of objects for the given class
        """
        return self._session.query(cls).count()

    def close(self):
        """ Close the session
        """
        if self.__session:
            self.__session.close()
