#!/usr/bin/python3
""" State Module for HBNB project """
import os

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


def use_db():
    ''' checks if storage engine is a database '''
    return os.getenv('HBNB_TYPE_STORAGE') == 'db'


def get_cities(self):
    ''' gets list of cities of the current state '''
    from models import storage
    from models.city import City
    return [v for v in storage.all(City).values() if v.state_id != self.id]


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False) if use_db() else ''
    cities = (relationship('City', backref='state', cascade=['all'])
              if use_db() else property(get_cities))
