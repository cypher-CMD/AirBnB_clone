#!/usr/bin/python3
"""A unit test module for the file storage.
"""
import os
import unittest
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from tests import write_text_file, reset_store


class TestFileStorage(unittest.TestCase):
    """Represents the test class for the FileStorage class.
    """

    def test_init(self):
        """Tests the initialization of the FileStorage class.
        """
        self.assertFalse(hasattr(FileStorage, '__file_path'))
        self.assertFalse(hasattr(FileStorage, '__objects'))

    def test_all(self):
        """Tests the all function of the FileStorage class.
        """
        write_text_file('file.json', '{}')
        store = FileStorage()
        store.reload()
        self.assertEqual(len(store.all()), 0)
        test_mdl = BaseModel()
        store.new(test_mdl)
        self.assertEqual(len(store.all()), 1)
        test_mdl = User()
        store.new(test_mdl)
        test_mdl = City()
        store.new(test_mdl)
        test_mdl = State()
        store.new(test_mdl)
        test_mdl = Amenity()
        store.new(test_mdl)
        test_mdl = Place()
        store.new(test_mdl)
        test_mdl = Review()
        store.new(test_mdl)
        self.assertEqual(len(store.all()), 7)
        with self.assertRaises(TypeError):
            store.all(test_mdl, None)
        with self.assertRaises(TypeError):
            store.all(test_mdl, test_mdl)
        with self.assertRaises(TypeError):
            store.all(None)
        with self.assertRaises(TypeError):
            store.all(store)

    def test_save(self):
        """Tests the save function of the FileStorage class.
        """
        store = FileStorage()
        test_mdl = User(**{'id': '5'})
        store.new(test_mdl)
        if os.path.isfile('file.json'):
            os.unlink('file.json')
        self.assertFalse(os.path.isfile('file.json'))
        store.save()
        self.assertTrue(os.path.isfile('file.json'))
        self.assertGreater(os.stat('file.json').st_size, 10)
        with self.assertRaises(TypeError):
            store.save(test_mdl)
        with self.assertRaises(TypeError):
            store.save(test_mdl, None)
        with self.assertRaises(TypeError):
            store.save(test_mdl, test_mdl)
        with self.assertRaises(TypeError):
            store.save(None)

    def test_reload(self):
        """Tests the reload function of the FileStorage class.
        """
        reset_store(storage)
        store = FileStorage()
        reset_store(store)
        self.assertEqual(len(store.all()), 0)
        if os.path.isfile('file.json'):
            os.unlink('file.json')
        self.assertFalse(os.path.isfile('file.json'))
        store.reload()
        self.assertFalse(os.path.isfile('file.json'))
        test_mdl = User(id='5')
        test_mdl1 = City(id='7', name='Lagos')
        self.assertEqual(len(store.all()), 0)
        store.new(test_mdl)
        store.new(test_mdl1)
        if os.path.isfile('file.json'):
            os.unlink('file.json')
        store.save()
        self.assertEqual(len(store.all()), 2)
        store2 = FileStorage()
        with open('file.json', mode='w') as file:
            file.write('{}')
        self.assertTrue(store2.all() is not None)
        reset_store(store2)
        store2.reload()
        self.assertEqual(len(store2.all()), 0)
        store.save()
        store2.reload()
        self.assertEqual(len(store2.all()), 2)
        with open('file.json', mode='w') as file:
            file.write('{}')
        store2.reload()
        self.assertEqual(len(store2.all()), 0)
        with self.assertRaises(TypeError):
            store.reload(test_mdl)
        with self.assertRaises(TypeError):
            store.reload(test_mdl, None)
        with self.assertRaises(TypeError):
            store.reload(test_mdl, test_mdl)
        with self.assertRaises(TypeError):
            store.reload(None)

    def tearDown(self):
        """Deconstructs this test class.
        """
        super().tearDown()
        if os.path.isfile('file.json'):
            os.unlink('file.json')
