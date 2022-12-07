#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.city import City


def use_db():
    ''' checks if storage engine is a database '''
    import os
    return os.getenv('HBNB_TYPE_STORAGE') == 'db'


class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.state_id),
                         str if not use_db() else type(None))

    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str if not use_db() else type(None))
