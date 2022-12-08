#!/usr/bin/python3
"""A unit test module for the console (command interpreter).
"""
import json
import MySQLdb
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch

from MySQLdb import connect

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream


host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
user = os.getenv('HBNB_MYSQL_USER')
passwd = os.getenv('HBNB_MYSQL_PWD')
dbname = os.getenv('HBNB_MYSQL_DB')


def rstr():
    ''' returns a random string'''
    import uuid
    return str(uuid.uuid4())


class TestHBNBCommand(unittest.TestCase):
    """ tests console class """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fcreate(self):
        """ tests create for file storage """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create City name="c1"')
            _id = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn('City.{}'.format(_id), storage.all().keys())
            cons.onecmd('show City {}'.format(_id))
            self.assertIn("'name': 'c1'", cout.getvalue().strip())
            clear_stream(cout)
            cons.onecmd('create User name="john" age=20 height=5')
            _id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(_id), storage.all().keys())
            clear_stream(cout)
            cons.onecmd('show User {}'.format(_id))
            self.assertIn("'name': 'john'", cout.getvalue().strip())
            self.assertIn("'height': 5", cout.getvalue().strip())
            self.assertIn("'age': 20", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """ tests count for db """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            db = connect(host=host, user=user, passwd=passwd, db=dbname)
            cur = db.cursor()

            cur.execute('SELECT COUNT(*) FROM states;')
            res = cur.fetchone()
            prev_count = int(res[0])
            cons.onecmd('create State name="s1"')
            clear_stream(cout)
            cons.onecmd('count State')
            cnt = cout.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(cout)
            cons.onecmd('count State')

            cur.close()
            db.close()
