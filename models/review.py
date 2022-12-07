#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


def use_db():
    ''' checks if storage engine is a database '''
    import os
    return os.getenv('HBNB_TYPE_STORAGE') == 'db'


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = 'reviews'
    place_id = (Column(String(60), ForeignKey('places.id'), nullable=False)
                if use_db() else '')
    user_id = (Column(String(60), ForeignKey('users.id'), nullable=False)
               if use_db() else '')
    text = Column(String(1024), nullable=False) if use_db() else ''
