#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


def use_db():
    ''' checks if storage engine is a database '''
    import os
    return os.getenv('HBNB_TYPE_STORAGE') == 'db'


class Amenity(BaseModel, Base):
    ''' class for amenities for stuff'''
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False) if use_db() else ''
