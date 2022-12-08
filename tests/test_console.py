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
    """Represents the test class for the HBNBCommand class. """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        """Tests the create command with the file storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create City name="Texas"')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            cons.onecmd('show City {}'.format(mdl_id))
            self.assertIn("'name': 'Texas'", cout.getvalue().strip())
            clear_stream(cout)
            cons.onecmd('create User name="James" age=17 height=5.9')
            mdl_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(mdl_id), storage.all().keys())
            clear_stream(cout)
            cons.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'name': 'James'", cout.getvalue().strip())
            self.assertIn("'age': 17", cout.getvalue().strip())
            self.assertIn("'height': 5.9", cout.getvalue().strip())

    # @unittest.skipIf(
    #     os.getenv('HBNB_TYPE_STORAGE') != '_db', 'DBStorage test')
    # def test_db_create(self):
    #     """Tests the create command with the database storage.
    #     """
    #     with patch('sys.stdout', new=StringIO()) as cout:
    #         cons = HBNBCommand()
    #         # creating a model with non-null attribute(s)
    #         with self.assertRaises(sqlalchemy.exc.OperationalError):
    #             cons.onecmd('create User')
    #         # creating a User instance
    #         clear_stream(cout)
            # cons.onecmd(
            #     'create User email="john25@gmail.com" password="123"')
    #         mdl_id = cout.getvalue().strip()

            # self.cur.execute('SELECT * FROM users WHERE id="{}"'.format(
            #     mdl_id))
    #         result = self.cur.fetchone()
    #         self.assertTrue(result is not None)
    #         self.assertIn('john25@gmail.com', result)
    #         self.assertIn('123', result)

    # @unittest.skipIf(
    #     os.getenv('HBNB_TYPE_STORAGE') != '_db', 'DBStorage test')
    # def test_db_show(self):
    #     """Tests the show command with the database storage.
    #     """
    #     with patch('sys.stdout', new=StringIO()) as cout:
    #         cons = HBNBCommand()
    #         # showing a User instance
    #         obj = User(email="john25@gmail.com", password="123")

            # self.cur.execute('SELECT * FROM users WHERE id="{}"'.format(
            #     obj.id))
    #         result = self.cur.fetchone()
    #         self.assertTrue(result is None)
    #         cons.onecmd('show User {}'.format(obj.id))
    #         self.assertEqual(
    #             cout.getvalue().strip(),
    #             '** no instance found **'
    #         )
    #         obj.save()

            # self.cur.execute('SELECT * FROM users WHERE id="{}"'.format(
            #     obj.id))
    #         clear_stream(cout)
    #         cons.onecmd('show User {}'.format(obj.id))
    #         result = self.cur.fetchone()
    #         self.assertTrue(result is not None)
    #         self.assertIn('john25@gmail.com', result)
    #         self.assertIn('123', result)
    #         self.assertIn('john25@gmail.com', cout.getvalue())
    #         self.assertIn('123', cout.getvalue())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            db = connect(host=host, user=user, passwd=passwd, db=dbname)
            cur = db.cursor()

            cur.execute('SELECT COUNT(*) FROM states;')
            res = cur.fetchone()
            prev_count = int(res[0])
            cons.onecmd('create State name="Enugu"')
            clear_stream(cout)
            cons.onecmd('count State')
            cnt = cout.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(cout)
            cons.onecmd('count State')

            cur.close()
            db.close()
