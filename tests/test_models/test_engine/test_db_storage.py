#!/usr/bin/python3
""" Module for testing db storage"""
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
port = 3306
user = os.getenv('HBNB_MYSQL_USER')
passwd = os.getenv('HBNB_MYSQL_PWD')
dbname = os.getenv('HBNB_MYSQL_DB')


def rstr():
    ''' returns a random string'''
    return str(uuid.uuid4())


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "Skipping db storage tests")
class test_dbStorage(unittest.TestCase):
    """ tests db_storage engine """
    def test_new(self):
        """ tests new objecct """
        new = User(email='abc@gmail.com', password='123',
                   first_name='john', last_name='doe')
        self.assertFalse(new in storage.all().values())
        new.save()
        self.assertTrue(new in storage.all().values())
        db = MySQLdb.connect(host=host, port=port, user=user,
                             passwd=passwd, db=dbname)
        cur = db.cursor()
        cur.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cur.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('abc@gmail.com', result)
        self.assertIn('123', result)
        self.assertIn('john', result)
        self.assertIn('doe', result)
        cur.close()
        db.close()

    def test_delete(self):
        """ tests deletion """
        new = User(email='abc@gmail.com', password='123',
                   first_name='john', last_name='doe')
        obj_key = 'User.{}'.format(new.id)
        db = MySQLdb.connect(host=host, port=port, user=user,
                             passwd=passwd, db=dbname)
        new.save()
        self.assertTrue(new in storage.all().values())
        cur = db.cursor()
        cur.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cur.fetchone()
        self.assertTrue(result is not None)
        self.assertIn('abc@gmail.com', result)
        self.assertIn('123', result)
        self.assertIn('john', result)
        self.assertIn('doe', result)
        self.assertIn(obj_key, storage.all(User).keys())
        new.delete()
        self.assertNotIn(obj_key, storage.all(User).keys())
        cur.close()
        db.close()

    def test_reload(self):
        """ reload """
        db = MySQLdb.connect(host=host, port=port, user=user,
                             passwd=passwd, db=dbname)
        cur = db.cursor()
        cur.execute(
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);',
            [
                '5566',
                str(datetime.utcnow()),
                str(datetime.utcnow()),
                'abc@gmail.com',
                '123',
                'john',
                'joe',
            ]
        )
        self.assertNotIn('User.5566', storage.all())
        db.commit()
        storage.reload()
        self.assertIn('User.5566', storage.all())
        cur.close()
        db.close()

    def test_save(self):
        """ tests saving """
        db = MySQLdb.connect(host=host, port=port, user=user,
                             passwd=passwd, db=dbname)
        new = User(email='abc@gmail.com', password='123',
                   first_name='john', last_name='doe')
        cur = db.cursor()
        cur.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cur.fetchone()
        cur.execute('SELECT COUNT(*) FROM users;')
        old_cnt = cur.fetchone()[0]
        self.assertTrue(result is None)
        self.assertFalse(new in storage.all().values())
        new.save()
        db1 = MySQLdb.connect(host=host, port=port, user=user,
                              passwd=passwd, db=dbname)
        cur1 = db1.cursor()
        cur1.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cur1.fetchone()
        cur1.execute('SELECT COUNT(*) FROM users;')
        new_cnt = cur1.fetchone()[0]
        self.assertFalse(result is None)
        self.assertEqual(old_cnt + 1, new_cnt)
        self.assertTrue(new in storage.all().values())
        cur1.close()
        db1.close()
        cur.close()
        db.close()

    def test_storage_var_created(self):
        """ testing storage type """
        from models.engine.db_storage import DBStorage

        self.assertEqual(type(storage), DBStorage)

    def test_new_and_save(self):
        '''testing  the new and save methods'''
        db = MySQLdb.connect(host=host, port=port, user=user,
                             passwd=passwd, db=dbname)

        new_user = User(**{'email': 'abc@gmail.com',
                           'password': 123,
                           'first_name': 'john',
                           'last_name': 'doe'})
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        old_count = cur.fetchall()
        cur.close()
        db.close()
        new_user.save()
        db = MySQLdb.connect(host=host, port=port, user=user,
                             passwd=passwd, db=dbname)
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        new_count = cur.fetchall()
        self.assertEqual(new_count[0][0], old_count[0][0] + 1)
        cur.close()
        db.close()
    # def __init__(self, *args, **kwargs):
    #     ''' setup cur and db '''
    #     super().__init__(*args, **kwargs)
    #     self.db = connect(host=host, user=user, passwd=passwd, db=dbname)
    #     self.db.autocommit(True)
    #     # self.cur = self.db.cursor()

    # def __del__(self):
    #     ''' free cur and db '''
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
