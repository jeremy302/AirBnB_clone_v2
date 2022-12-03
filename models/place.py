#!/usr/bin/python3
""" Place Module for HBNB project """
import os

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


def use_db():
    ''' checks if storage engine is a database '''
    return os.getenv('HBNB_TYPE_STORAGE') == 'db'


def get_reviews(self):
    ''' gets list of reviews of the current place '''
    from models import storage
    from models.review import Review

    return [v for v in storage.all(Review).values() if v.place_id == self.id]


def get_amenities(self):
    ''' gets list of amenities of the current place '''
    from models import storage
    from models.amenity import Amenity

    return [v for v in storage.all(Amenity).values()
            if v.id in self.amenity_ids]


def set_amenities(self, ls):
    ''' sets list of amenities of the current place '''
    from models import storage
    from models.amenity import Amenity

    self.amenity_ids = [v.id for v in ls]


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Integer)
    longitude = Column(Integer)
    amenity_ids = []

    reviews = (relationship('Review', backref='place', cascade='all')
               if use_db() else property(get_reviews))
    amenities = (relationship('Amenity',
                              secondary=place_amenity, viewonly=False)
                 if use_db() else property(get_amenities, set_amenities))
