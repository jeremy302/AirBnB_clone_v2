#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table


class Amenity(BaseModel, Base):
    ''' class for amenities for stuff'''
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)

    # place_amenities = relationship('Place',)
