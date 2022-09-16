#!/usr/bin/python3
"""Unit test module for the base model of all models.
"""
from models.base_model import BaseModel
from tests import write_text_file
import os
import unittest
from datetime import datetime
from time import sleep


class TestBaseModel(unittest.TestCase):
    """Test class for the BaseModel class.
    """

    def test_init(self):
        """Tests the initialization of the BaseModel class.
        """
        self.assertFalse(hasattr(BaseModel, 'id'))
        self.assertFalse(hasattr(BaseModel, 'created_at'))
        self.assertFalse(hasattr(BaseModel, 'updated_at'))
        self.assertTrue(hasattr(BaseModel(), 'id'))
        self.assertTrue(hasattr(BaseModel(), 'created_at'))
        self.assertTrue(hasattr(BaseModel(), 'updated_at'))
        self.assertIsInstance(BaseModel().id, str)
        self.assertIsInstance(BaseModel().created_at, datetime)
        self.assertIsInstance(BaseModel().updated_at, datetime)
        # Tests for the uniqueness in ID's
        test_mdl1 = BaseModel()
        test_mdl2 = BaseModel()
        self.assertNotEqual(test_mdl1.id, test_mdl2.id)
        # Tests for differences in created time
        test_mdl3 = BaseModel()
        sleep(0.06)
        test_mdl4 = BaseModel()
        self.assertLess(test_mdl3.created_at, test_mdl4.created_at)
        # Tests for differences in updated time
        test_mdl3 = BaseModel()
        sleep(0.06)
        test_mdl4 = BaseModel()
        self.assertLess(test_mdl3.updated_at, test_mdl4.updated_at)
        # Tests for unused args
        test_mdl = BaseModel(None)
        self.assertNotIn(None, test_mdl.__dict__.values())
        # Tests instantiation with kwargs
        datetime_now = datetime.today()
        datetime_iso = datetime_now.isoformat()
        test_mdl = BaseModel(
            id='012',
            created_at=datetime_iso,
            updated_at=datetime_iso
        )
        self.assertEqual(test_mdl.id, '012')
        self.assertEqual(test_mdl.created_at, datetime_now)
        self.assertEqual(test_mdl.updated_at, datetime_now)
        # Tests instantiations with None kwargs
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)
        # Tests instantiation with args and kwargs
        datetime_now = datetime.today()
        datetime_iso = datetime_now.isoformat()
        test_mdl = BaseModel(
            '01', id='012', created_at=datetime_iso,
            updated_at=datetime_iso
        )
        self.assertEqual(test_mdl.id, '012')
        self.assertEqual(test_mdl.created_at, datetime_now)
        self.assertEqual(test_mdl.updated_at, datetime_now)
        self.assertEqual(BaseModel(id=45).id, 45)
        self.assertEqual(BaseModel(id=None).id, None)
        self.assertNotEqual(BaseModel('jfk1').id, 'jfk1')
        self.assertNotEqual(BaseModel('jfk1').created_at, 'jfk1')
        self.assertNotEqual(BaseModel('jfk1').updated_at, 'jfk1')
        self.assertTrue(hasattr(BaseModel(foo=45), 'foo'))
        self.assertFalse(hasattr(BaseModel(foo=45), 'id'))
        self.assertFalse(hasattr(BaseModel(foo=45), 'created_at'))
        self.assertFalse(hasattr(BaseModel(foo=45), 'updated_at'))
        self.assertNotEqual(BaseModel(__class__='45').__class__, '45')
        self.assertNotEqual(BaseModel(__class__=None).__class__, None)
        with self.assertRaises(TypeError):
            BaseModel(**{'created_at': 45})
        with self.assertRaises(TypeError):
            BaseModel(**{'created_at': datetime.now()})
        with self.assertRaises(TypeError):
            BaseModel(**{'updated_at': 45})
        with self.assertRaises(TypeError):
            BaseModel(**{'updated_at': datetime.now()})

    def test_str(self):
        """Tests the __str__ representation function of the BaseModel class.
        """
        datetime_now = datetime.today()
        datetime_repr = repr(datetime_now)
        test_mdl = BaseModel()
        test_mdl.id = '012345'
        test_mdl.created_at = test_mdl.updated_at = datetime_now
        test_mdl_str = str(test_mdl)
        self.assertIn("[BaseModel] (012345)", test_mdl_str)
        self.assertIn("'id': '012345'", test_mdl_str)
        self.assertIn("'created_at': " + datetime_repr, test_mdl_str)
        self.assertIn("'updated_at': " + datetime_repr, test_mdl_str)
        self.assertIn("'id': ", str(BaseModel()))
        self.assertIn("'created_at': ", str(BaseModel()))
        self.assertIn("'updated_at': ", str(BaseModel()))
        self.assertIn(
            "'gender': 'female'",
            str(BaseModel(gender='female', id='m-77'))
        )
        self.assertIn(
            "'id': 'm-77'",
            str(BaseModel(gender='female', id='m-77'))
        )
        self.assertNotIn(
            "'created_at': ",
            str(BaseModel(gender='female', id='u-88'))
        )
        self.assertNotIn(
            "'updated_at': ",
            str(BaseModel(gender='female', id='u-55'))
        )
        self.assertRegex(
            str(BaseModel()),
            r'\[BaseModel\] \([0-9a-zA-Z]+(?:-[0-9a-zA-Z]+)*\) \{.+\}'
        )
        self.assertEqual(
            str(BaseModel(id='m-345')),
            "[BaseModel] (m-345) {'id': 'm-345'}"
        )
        self.assertEqual(
            str(BaseModel(id=45)),
            "[BaseModel] (45) {'id': 45}"
        )
        self.assertEqual(
            str(BaseModel(id=None)),
            "[BaseModel] (None) {'id': None}"
        )
        with self.assertRaises(AttributeError):
            str(BaseModel(gender='female'))

    def test_save(self):
        """Tests the save function of the BaseModel class.
        """
        if os.path.isfile('file.json'):
            os.unlink('file.json')
        self.assertFalse(os.path.isfile('file.json'))
        test_mdl = BaseModel(id='this -is-a-unique-id')
        self.assertFalse(hasattr(test_mdl, 'updated_at'))
        test_mdl.save()
        self.assertTrue(hasattr(test_mdl, 'updated_at'))
        self.assertTrue(os.path.isfile('file.json'))
        self.assertGreater(os.stat('file.json').st_size, 15)
        with self.assertRaises(TypeError):
            BaseModel().save(test_mdl)
        with self.assertRaises(TypeError):
            BaseModel().save(BaseModel())
        with self.assertRaises(TypeError):
            BaseModel().save(None)
        # Tests save updates on file
        write_text_file('file.json', '{}')
        test_mdl = BaseModel()
        test_mdl.save()
        with open('file.json', 'r') as f:
            line = f.readline()
            self.assertIn('"id": ', line)
            self.assertIn('"created_at": ', line)
            self.assertIn('"updated_at": ', line)

    def test_to_dict(self):
        """Tests the to_dict function of the BaseModel class.
        """
        # Tests if it's a dictionary
        self.assertIsInstance(BaseModel().to_dict(), dict)
        # Tests if to_dict contains accurate keys
        self.assertIn('id', BaseModel().to_dict())
        self.assertIn('created_at', BaseModel().to_dict())
        self.assertIn('updated_at', BaseModel().to_dict())
        # Tests if to_dict contains added attributes
        test_mdl = BaseModel()
        test_mdl.firstname = 'George'
        test_mdl.lastname = 'Jungle'
        self.assertIn('firstname', test_mdl.to_dict())
        self.assertIn('lastname', test_mdl.to_dict())
        self.assertIn('firstname', BaseModel(firstname='George').to_dict())
        self.assertIn('lastname', BaseModel(lastname='Jungle').to_dict())
        # Tests to_dict datetime attributes if they are strings
        self.assertIsInstance(BaseModel().to_dict()['created_at'], str)
        self.assertIsInstance(BaseModel().to_dict()['updated_at'], str)
        # Tests to_dict output
        datetime_now = datetime.today()
        test_mdl = BaseModel()
        test_mdl.id = '012345'
        test_mdl.created_at = test_mdl.updated_at = datetime_now
        to_dict = {
            'id': '012345',
            '__class__': 'BaseModel',
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(test_mdl.to_dict(), to_dict)
        self.assertDictEqual(
            BaseModel(id='u-b34', age=13).to_dict(),
            {
                '__class__': 'BaseModel',
                'id': 'u-b34',
                'age': 13
            }
        )
        self.assertDictEqual(
            BaseModel(id='u-b34', age=None).to_dict(),
            {
                '__class__': 'BaseModel',
                'id': 'u-b34',
                'age': None
            }
        )
        # Tests to_dict output contradiction
        test_mdl_d = BaseModel()
        self.assertIn('__class__', BaseModel().to_dict())
        self.assertNotIn('__class__', BaseModel().__dict__)
        self.assertNotEqual(test_mdl_d.to_dict(), test_mdl_d.__dict__)
        self.assertNotEqual(
            test_mdl_d.to_dict()['__class__'],
            test_mdl_d.__class__
        )
        # Tests to_dict with arg
        with self.assertRaises(TypeError):
            BaseModel().to_dict(None)
        with self.assertRaises(TypeError):
            BaseModel().to_dict(BaseModel())
        with self.assertRaises(TypeError):
            BaseModel().to_dict(45)

    def tearDown(self):
        """Deconstructs this test class.
        """
        super().tearDown()
        if os.path.isfile('file.json'):
            os.unlink('file.json')
