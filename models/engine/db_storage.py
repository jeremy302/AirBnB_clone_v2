#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage():
    __engine = None
    __session = None

    def __init__(self):
        ''' creates an engine, and drops tables when in a test environment'''
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        dbname = os.getenv('HBNB_MYSQL_DB')
        is_test = os.getenv('HBNB_ENV') == 'test'
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, dbname),
                                      pool_pre_ping=True)
        if is_test:
            from models.base_model import Base
            Base.metadata.drop_all(self.__engine)

    def get_session(self):
        ''' gets the database session, or create a new one if none exists'''
        # if not self.__session:
        #     self.__session = sessionmaker(bind=self.__engine)() # ()?
        # if self.__session:
        #     return self.__session()
        # self.reload()
        return self.__session()

    def all(self, cls=None):
        ''' returns all objects of a class '''
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = ((cls,) if cls else
                   (User, Place, State, City, Amenity, Review))
        sess = self.get_session()
        all = {}

        for c in classes:
            for obj in sess.query(c):
                key = obj.to_dict()['__class__'] + '.' + obj.id
                all[key] = obj
        return all

    def new(self, obj):
        ''' adds an object to the database session '''
        sess = self.get_session()
        sess.add(obj)

    def save(self):
        ''' commit changes in the current session to the database  '''
        sess = self.get_session()
        sess.commit()

    def delete(self, obj=None):
        ''' deletes an object from the database '''
        if obj:
            sess = self.get_session()
            sess.delete(obj)
            sess.commit()

    def reload(self):
        ''' reloads data from the database '''
        from models.base_model import Base, BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        Base.metadata.create_all(self.__engine)

        if self.__session:
            self.__session.remove()
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)
