#!/usr/bin/python3
""" Module for testing file storage"""
import os
import unittest

from models.base_model import BaseModel
from models import storage


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'file',
                 "Skipping file storage tests")
class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        storage.all().clear()

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is added to __objects after only saving """
        new = BaseModel()
        # for obj in storage.all().values():
        #     temp = obj
        self.assertTrue(new not in storage.all().values())
        new.save()
        self.assertTrue(new in storage.all().values())

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        new.save()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File IS created on BaseModel save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        new.save()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        new.save()
        storage.reload()
        items = list(storage.all().values())
        loaded = items[0]
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        new.save()
        _id = new.to_dict()['id']
        temp = list(storage.all().keys())[0]
        # for key in storage.all().keys():
        #     temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        # print(type(storage))
        self.assertEqual(type(storage), FileStorage)

    def test_delete(self):
        ''' tests if objects are deleted'''
        new = BaseModel()
        new.save()
        self.assertTrue(new in storage.all().values())
        storage.delete(new)
        self.assertEqual(storage.all(), {})

    def test_all(self):
        ''' test all() for different classes '''
        from models.amenity import Amenity

        obj1 = BaseModel()
        obj2 = Amenity()
        obj1.save()
        obj2.save()
        self.assertTrue(obj1 in storage.all().values() and
                        obj2 in storage.all().values())
        self.assertTrue(obj1 in storage.all(BaseModel).values() and
                        obj2 not in storage.all(BaseModel).values())
        self.assertTrue(obj1 not in storage.all(Amenity).values() and
                        obj2 in storage.all(Amenity).values())
