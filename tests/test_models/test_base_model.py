#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
from datetime import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_default(self):
        """ """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'For file storage')
    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ tests str() function """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ testing to_dict() """

        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)
        self.assertIsInstance(self.value().to_dict(), dict)
        self.assertIn('id', self.value().to_dict())
        self.assertIn('created_at', self.value().to_dict())
        self.assertIn('updated_at', self.value().to_dict())
        self.assertIsInstance(self.value().to_dict()['created_at'], str)
        self.assertIsInstance(self.value().to_dict()['updated_at'], str)

        obj = self.value()
        obj.abc = '123'
        self.assertIn('abc', obj.to_dict())
        self.assertIn('abc', self.value(abc='123').to_dict())

        datetime_now = datetime.today()
        obj = self.value()
        obj.id = 'abcd'
        obj.created_at = datetime_now
        obj.updated_at = datetime_now
        to_dict = {
            'id': 'abcd',
            '__class__': obj.__class__.__name__,
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(obj.to_dict(), to_dict)
        # if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        #     print(self.value(id='abcde'))
        #     self.assertEqual(self.value(id='abcde').to_dict(),
        #                      {'__class__': obj.__class__.__name__,
        #                       'id': 'abcde'})

        obj = self.value()
        self.assertIn('__class__', self.value().to_dict())
        self.assertNotIn('__class__', self.value().__dict__)
        self.assertNotEqual(obj.to_dict(), obj.__dict__)
        self.assertNotEqual(obj.to_dict()['__class__'], obj.__class__)

        with self.assertRaises(TypeError):
            self.value().to_dict(None)
        self.assertNotIn('_sa_instance_state', n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ """
        n = {'Name': 'test'}
        new = self.value(**n)
        self.assertEqual(hasattr(new, 'Name'), True)

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'for file storage')
    def test_delete(self):
        """ testing delete function """
        from models import storage

        obj = self.value()
        obj.save()
        self.assertEqual(obj in storage.all().values(), True)
        obj.delete()
        self.assertEqual(obj in storage.all().values(), False)

    def test_updated_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)
