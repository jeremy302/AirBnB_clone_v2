#!/usr/bin/python3
""" Module for testing file storage"""
import os
import uuid
import unittest
from datetime import datetime

import MySQLdb
from MySQLdb import connect

from models import storage
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
user = os.getenv('HBNB_MYSQL_USER')
passwd = os.getenv('HBNB_MYSQL_PWD')
dbname = os.getenv('HBNB_MYSQL_DB')


def rstr():
    ''' returns a random string'''
    return str(uuid.uuid4())


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "Skipping db storage tests")
class test_dbStorage(unittest.TestCase):
    """ Class to test the db storage method """
    def __init__(self, *args, **kwargs):
        ''' setup cursor and db '''
        super().__init__(*args, **kwargs)
        self.db = connect(host=host, user=user, passwd=passwd, db=dbname)
        self.db.autocommit(True)
        # self.cur = self.db.cursor()

    def __del__(self):
        ''' free cursor and db '''
        # self.cur.close()
        self.db.close()

    def setUp(self):
        """ Set up test environment """
        self.cur = self.db.cursor()

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            self.cur.close()
        except Exception:
            pass

    def test_new(self):
        """ New object is added to __objects after only saving """
        s = rstr()
        new = State(name=s)
        new.save()
        self.cur.execute(f'SELECT * FROM states WHERE id="{new.id}";')
        row = self.cur.fetchone()
        self.assertTrue(row is not None and s in row)

    def test_all(self):
        """ __objects is properly returned """
        self.assertIsInstance(storage.all(), dict)

        new = State(name=rstr())
        self.assertTrue(new not in storage.all().values())
        new.save()
        self.assertTrue(new in storage.all().values())
        self.assertTrue(new in storage.all(State).values())
        self.assertTrue(new not in storage.all(Place).values())

    def test_reload(self):
        ''' testing reload function '''
        s1 = rstr()
        s2 = rstr()
        d = str(datetime.utcnow())

        self.cur.execute('INSERT INTO amenities ' +
                         '(id, created_at, updated_at, name) VALUES ' +
                         '(%s, %s, %s, %s)',
                         [s1, d, d, s2])
        storage.reload()
        self.assertTrue(any(True for v in storage.all(Amenity).values()
                            if v.id == s1 and v.name == s2))

    def test_delete(self):
        ''' testing delete function '''
        new = State(name=rstr())
        new.save()
        storage.delete(new)
        self.cur.execute(f'SELECT * FROM states WHERE id="{new.id}"')
        self.assertEqual(self.cur.fetchone(), None)

    def test_save(self):
        ''' testing save function '''
        new = State(name=rstr())
        self.cur.execute(f'SELECT * FROM states WHERE id="{new.id}"')
        self.assertEqual(self.cur.fetchone(), None)
        new.save()
        self.cur.execute(f'SELECT * FROM states WHERE id="{new.id}"')
        self.assertTrue(self.cur.fetchone() is not None)

    def test_key_format(self):
        """ Key is properly formatted """
        new = State(name=rstr())
        new.save()

        key = 'State' + '.' + new.to_dict()['id']
        self.assertEqual(storage.all()[key], new)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.db_storage import DBStorage

        self.assertEqual(type(storage), DBStorage)
