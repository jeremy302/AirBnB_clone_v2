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
    def test_new(self):
        """ New object is correctly added to database """
        new = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        self.assertFalse(new in storage.all().values())
        new.save()
        self.assertTrue(new in storage.all().values())
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('john2020@gmail.com', result)
        self.assertIn('password', result)
        self.assertIn('John', result)
        self.assertIn('Zoldyck', result)
        cursor.close()
        dbc.close()

    def test_delete(self):
        """ Object is correctly deleted from database """
        new = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        obj_key = 'User.{}'.format(new.id)
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        new.save()
        self.assertTrue(new in storage.all().values())
        cursor = dbc.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('john2020@gmail.com', result)
        self.assertIn('password', result)
        self.assertIn('John', result)
        self.assertIn('Zoldyck', result)
        self.assertIn(obj_key, storage.all(User).keys())
        new.delete()
        self.assertNotIn(obj_key, storage.all(User).keys())
        cursor.close()
        dbc.close()

    def test_reload(self):
        """ Tests the reloading of the database session """
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute(
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);',
            [
                '4448-by-me',
                str(datetime.now()),
                str(datetime.now()),
                'ben_pike@yahoo.com',
                'pass',
                'Benjamin',
                'Pike',
            ]
        )
        self.assertNotIn('User.4448-by-me', storage.all())
        dbc.commit()
        storage.reload()
        self.assertIn('User.4448-by-me', storage.all())
        cursor.close()
        dbc.close()

    def test_save(self):
        """ object is successfully saved to database """
        new = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) FROM users;')
        old_cnt = cursor.fetchone()[0]
        self.assertTrue(result is None)
        self.assertFalse(new in storage.all().values())
        new.save()
        dbc1 = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor1 = dbc1.cursor()
        cursor1.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor1.fetchone()
        cursor1.execute('SELECT COUNT(*) FROM users;')
        new_cnt = cursor1.fetchone()[0]
        self.assertFalse(result is None)
        self.assertEqual(old_cnt + 1, new_cnt)
        self.assertTrue(new in storage.all().values())
        cursor1.close()
        dbc1.close()
        cursor.close()
        dbc.close()

    def test_storage_var_created(self):
        """ DBStorage object storage created """
        from models.engine.db_storage import DBStorage
        self.assertEqual(type(storage), DBStorage)

    def test_new_and_save(self):
        '''testing  the new and save methods'''
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        new_user = User(**{'first_name': 'jack',
                           'last_name': 'bond',
                           'email': 'jack@bond.com',
                           'password': 12345})
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        old_count = cur.fetchall()
        cur.close()
        db.close()
        new_user.save()
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        new_count = cur.fetchall()
        self.assertEqual(new_count[0][0], old_count[0][0] + 1)
        cur.close()
        db.close()
    # def __init__(self, *args, **kwargs):
    #     ''' setup cursor and db '''
    #     super().__init__(*args, **kwargs)
    #     self.db = connect(host=host, user=user, passwd=passwd, db=dbname)
    #     self.db.autocommit(True)
    #     # self.cur = self.db.cursor()

    # def __del__(self):
    #     ''' free cursor and db '''
    #     # self.cur.close()
    #     self.db.close()

    # def setUp(self):
    #     """ Set up test environment """
    #     self.cur = self.db.cursor()

    # def tearDown(self):
    #     """ Remove storage file at end of tests """
    #     try:
    #         self.cur.close()
    #     except Exception:
    #         pass

    # def test_new(self):
    #     """ New object is added to __objects after only saving """
    #     s = rstr()
    #     new = State(name=s)
    #     new.save()
    #     self.cur.execute(f'SELECT * FROM states WHERE id="{new.id}";')
    #     row = self.cur.fetchone()
    #     self.assertTrue(row is not None and s in row)

    # def test_all(self):
    #     """ __objects is properly returned """
    #     self.assertIsInstance(storage.all(), dict)

    #     new = State(name=rstr())
    #     self.assertTrue(new not in storage.all().values())
    #     new.save()
    #     self.assertTrue(new in storage.all().values())
    #     self.assertTrue(new in storage.all(State).values())
    #     self.assertTrue(new not in storage.all(Place).values())

    # def test_reload(self):
    #     ''' testing reload function '''
    #     s1 = rstr()
    #     s2 = rstr()
    #     d = str(datetime.utcnow())

    #     self.cur.execute('INSERT INTO amenities ' +
    #                      '(id, created_at, updated_at, name) VALUES ' +
    #                      '(%s, %s, %s, %s)',
    #                      [s1, d, d, s2])
    #     storage.reload()
    #     self.assertTrue(any(True for v in storage.all(Amenity).values()
    #                         if v.id == s1 and v.name == s2))

    # def test_delete(self):
    #     ''' testing delete function '''
    #     new = State(name=rstr())
    #     new.save()
    #     storage.delete(new)
    #     self.cur.execute(f'SELECT * FROM states WHERE id="{new.id}"')
    #     self.assertEqual(self.cur.fetchone(), None)

    # def test_save(self):
    #     ''' testing save function '''
    #     new = State(name=rstr())
    #     self.cur.execute(f'SELECT * FROM states WHERE id="{new.id}"')
    #     self.assertEqual(self.cur.fetchone(), None)
    #     new.save()
    #     self.cur.execute(f'SELECT * FROM states WHERE id="{new.id}"')
    #     self.assertTrue(self.cur.fetchone() is not None)

    # def test_key_format(self):
    #     """ Key is properly formatted """
    #     new = State(name=rstr())
    #     new.save()

    #     key = 'State' + '.' + new.to_dict()['id']
    #     self.assertEqual(storage.all()[key], new)

    # def test_storage_var_created(self):
    #     """ FileStorage object storage created """
    #     from models.engine.db_storage import DBStorage

    #     self.assertEqual(type(storage), DBStorage)
