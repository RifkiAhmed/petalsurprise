#!/usr/bin/python3
"""
DB model
"""
from models.basemodel import Base
from sqlalchemy import create_engine, and_, func
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from os import getenv


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """ Initialize a new DB instance
        """
        self._engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                     format(getenv('DB_USER'),
                                            getenv('DB_PWD'),
                                            getenv('DB_HOST'),
                                            getenv('DB_NAME')))
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memoized session object
        """
        Base.metadata.create_all(self._engine)
        if self.__session is None:
            sess_factory = sessionmaker(
                bind=self._engine, expire_on_commit=False)
            DBSession = scoped_session(sess_factory)
            self.__session = DBSession()

        return self.__session

    def all(self, cls):
        """ Returns all the object of the given cls argument
        """
        return self._session.query(cls).all()

    def add(self, obj):
        """ Add a new object to the database
        """
        if obj:
            self._session.add(obj)
            self._session.commit()

    def delete(self, obj):
        """ Delete the object from the database
        """
        if obj:
            self._session.delete(obj)
            self._session.commit()

    def save(self):
        """ Save change to the database
        """
        if self._session:
            self._session.commit()

    def get_limit(self, cls, page, per_page, sort_by=None):
        """ Returns the objects corresponding to the page of size per_page
        """
        query = self._session.query(cls).filter(cls.listed == 1)
        count_listed = self._session.query(cls).filter(cls.listed == 1).count()

        if sort_by == 'recent_listing':
            query = query.order_by(cls.id.desc())
        elif sort_by == 'low_to_high':
            query = query.order_by(cls.price)
        elif sort_by == 'high_to_low':
            query = query.order_by(cls.price.desc())
        else:
            count = self.count(cls)
            start = page * per_page
            end = (start + per_page) if (start + per_page) < count else count
            query = query.order_by(cls.id.desc()).slice(start, end)

        products = query.all()
        return products, count_listed

    def get_range_filter(self, cls, min_price, max_price):
        """ Returns the objects within a specified price range
        """
        query = self._session.query(cls).filter(cls.listed)

        if min_price is not None:
            query = query.filter(cls.price >= min_price)
        if max_price is not None:
            query = query.filter(cls.price <= max_price)
        products = query.all()

        return products

    def get_string_filter(self, cls, search_name):
        """ Returns the objects whose name contains a given pattern
        """
        query = self._session.query(cls).filter(cls.listed)

        if search_name:
            query = query.filter(cls.name.like(f'%{search_name}%'))
        products = query.all()

        return products

    def find_by(self, cls, **kwargs):
        """ Returns the first object based on the given keyword argument
        """
        obj = self._session.query(cls).filter_by(**kwargs).first()

        if not obj:
            raise NoResultFound

        return obj

    def find_all(self, cls, **kwargs):
        """ Returns all the objects based on the given keyword argument
        """
        objs = self._session.query(cls).filter_by(**kwargs).all()

        if objs is None:
            raise NoResultFound

        return objs

    def orders_overview(self, cls):
        """ Returns orders stats
        """
        stats_1 = self._session.query(
            cls.status,
            func.count(cls.id).label('count_orders'),
            func.sum(cls.amount).label('total_amount')) \
            .group_by(cls.status) \
            .all()

        stats_2 = self._session.query(
            func.date(cls.created_at).label('creation_date'),
            func.count(cls.id).label('count_orders'),
            func.sum(cls.amount).label('total_amount')) \
            .group_by(func.date(cls.created_at)) \
            .all()

        if stats_1 is None and stats_2 is None:
            raise NoResultFound

        return [stats_1, stats_2]

    def update(self, obj, **kwargs) -> None:
        """ Updates object attributes with the given key-value pairs
        """
        try:
            if obj:
                for key, value in kwargs.items():
                    if key in obj.__dict__:
                        setattr(obj, key, value)
                    else:
                        raise ValueError
                self._session.commit()
        except IntegrityError:
            raise ValueError

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
