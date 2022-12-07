#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


def use_db():
    ''' checks if storage engine is a database '''
    import os
    return os.getenv('HBNB_TYPE_STORAGE') == 'db'


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    state_id = (Column(String(60), ForeignKey("states.id"), nullable=False)
                if use_db() else '')
    name = (Column(String(128), nullable=False) if use_db() else '')

    places = (relationship('Place', backref='cities', cascade='all')
              if use_db() else None)
