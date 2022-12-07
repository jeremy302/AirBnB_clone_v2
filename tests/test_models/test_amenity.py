#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity


def use_db():
    ''' checks if storage engine is a database '''
    import os
    return os.getenv('HBNB_TYPE_STORAGE') == 'db'


class test_Amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ constructor """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """ testing name """
        new = self.value()
        if use_db():
            self.assertEqual(new.name, None)
        else:
            self.assertEqual(type(new.name), str)
