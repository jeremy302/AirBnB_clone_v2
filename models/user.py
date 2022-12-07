#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


def use_db():
    ''' checks if storage engine is a database '''
    import os
    return os.getenv('HBNB_TYPE_STORAGE') == 'db'


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False) if use_db() else ''
    password = Column(String(128), nullable=False) if use_db() else ''
    first_name = Column(String(128), nullable=True) if use_db() else ''
    last_name = Column(String(128), nullable=True) if use_db() else ''

    places = (relationship('Place', backref='user', cascade='all')
              if use_db() else None)
    reviews = (relationship('Review', backref='user', cascade='all')
               if use_db() else None)
