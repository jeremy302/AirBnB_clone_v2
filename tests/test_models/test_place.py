#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.place import Place


def use_db():
    ''' checks if storage engine is a database '''
    import os
    return os.getenv('HBNB_TYPE_STORAGE') == 'db'


class test_Place(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.city_id), str
                         if not use_db() else type(None))

    def test_user_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.user_id), str
                         if not use_db() else type(None))

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str
                         if not use_db() else type(None))

    def test_description(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.description), str
                         if not use_db() else type(None))

    def test_number_rooms(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.number_rooms), int
                         if not use_db() else type(None))

    def test_number_bathrooms(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.number_bathrooms), int
                         if not use_db() else type(None))

    def test_max_guest(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.max_guest), int
                         if not use_db() else type(None))

    def test_price_by_night(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.price_by_night), int
                         if not use_db() else type(None))

    def test_latitude(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.latitude), float
                         if not use_db() else type(None))

    def test_longitude(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.latitude), float
                         if not use_db() else type(None))

    def test_amenity_ids(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.amenity_ids), list)
