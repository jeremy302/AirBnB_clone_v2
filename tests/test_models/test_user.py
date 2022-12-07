#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.user import User


def use_db():
    ''' checks if storage engine is a database '''
    import os
    return os.getenv('HBNB_TYPE_STORAGE') == 'db'


class test_User(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.first_name), str
                         if not use_db() else type(None))

    def test_last_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.last_name), str
                         if not use_db() else type(None))

    def test_email(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.email), str if not use_db() else type(None))

    def test_password(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.password), str
                         if not use_db() else type(None))
