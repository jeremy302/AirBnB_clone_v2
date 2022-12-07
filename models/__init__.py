#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os

storage = None


def use_db():
    ''' checks if storage engine is a database '''
    return os.getenv('HBNB_TYPE_STORAGE') == 'db'


if use_db():
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()

if True:
    from models.base_model import Base, BaseModel
    from models.user import User
    from models.place import Place
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.review import Review
