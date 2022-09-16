#!/usr/bin/python3
"""unit test module for the city model.
"""
from models.base_model import BaseModel
from models.city import City
import os
import unittest
from datetime import datetime


class TestCity(unittest.TestCase):
    """class for the City class test
    """

    def test_init(self):
        """Tests initialization of the City class.
        """
        self.assertIsInstance(City(), BaseModel)
        self.assertTrue(hasattr(City, 'name'))
        self.assertTrue(hasattr(City, 'state_id'))
        self.assertIsInstance(City.name, str)
        self.assertIsInstance(City.state_id, str)
        self.assertEqual(City().name, '')
        self.assertEqual(City().state_id, '')
        self.assertEqual(City('Enugu').name, '')
        self.assertEqual(City('9e4d').state_id, '')
        self.assertEqual(City(name='Abakpa').name, 'Abakpa')
        self.assertEqual(City(state_id='9e45').state_id, '9e45')
        self.assertEqual(City('New Jersey', name='Quohug').name, 'Quohug')
        self.assertEqual(City('32f5', state_id='9e4d').state_id, '9e4d')

    def test_str(self):
        """Tests the __str__ representation function of the City class.
        """
        datetime_now = datetime.today()
        datetime_repr = repr(datetime_now)
        test_mdl = City()
        test_mdl.id = '012345'
        test_mdl.created_at = test_mdl.updated_at = datetime_now
        test_mdl_str = str(test_mdl)
        self.assertIn("[City] (012345)", test_mdl_str)
        self.assertIn("'id': '012345'", test_mdl_str)
        self.assertIn("'created_at': " + datetime_repr, test_mdl_str)
        self.assertIn("'updated_at': " + datetime_repr, test_mdl_str)
        self.assertIn("'id': ", str(City()))
        self.assertIn("'created_at': ", str(City()))
        self.assertIn("'updated_at': ", str(City()))
        self.assertIn(
            "'gender': 'female'",
            str(City(gender='female', id='m-77'))
        )
        self.assertNotIn(
            "'created_at': ",
            str(City(gender='female', id='u-88'))
        )
        self.assertNotIn(
            "'updated_at': ",
            str(City(gender='female', id='u-55'))
        )
        self.assertRegex(
            str(City()),
            r'\[City\] \([0-9a-zA-Z]+(?:-[0-9a-zA-Z]+)*\) \{.+\}'
        )
        self.assertEqual(
            str(City(id='m-345')),
            "[City] (m-345) {'id': 'm-345'}"
        )
        self.assertEqual(
            str(City(id=45)),
            "[City] (45) {'id': 45}"
        )
        self.assertEqual(
            str(City(id=None)),
            "[City] (None) {'id': None}"
        )
        with self.assertRaises(AttributeError):
            str(City(gender='female'))

    def test_to_dict(self):
        """Tests the to_dict function of the City class.
        """
        # Tests if it's a dictionary
        self.assertIsInstance(City().to_dict(), dict)
        # Tests if to_dict contains accurate keys
        self.assertIn('id', City().to_dict())
        self.assertIn('created_at', City().to_dict())
        self.assertIn('updated_at', City().to_dict())
        # Tests if to_dict contains added attributes
        test_mdl = City()
        test_mdl.firstname = 'George'
        test_mdl.lastname = 'Jungle'
        self.assertIn('firstname', test_mdl.to_dict())
        self.assertIn('lastname', test_mdl.to_dict())
        self.assertIn('firstname', City(firstname='George').to_dict())
        self.assertIn('lastname', City(lastname='Jungle').to_dict())
        # Tests to_dict datetime attributes if they are strings
        self.assertIsInstance(City().to_dict()['created_at'], str)
        self.assertIsInstance(City().to_dict()['updated_at'], str)
        # Tests to_dict output
        datetime_now = datetime.today()
        test_mdl = City()
        test_mdl.id = '012345'
        test_mdl.created_at = test_mdl.updated_at = datetime_now
        to_dict = {
            'id': '012345',
            '__class__': 'City',
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(test_mdl.to_dict(), to_dict)
        self.assertDictEqual(
            City(id='u-b34', age=13).to_dict(),
            {
                '__class__': 'City',
                'id': 'u-b34',
                'age': 13
            }
        )
        self.assertDictEqual(
            City(id='u-b34', age=None).to_dict(),
            {
                '__class__': 'City',
                'id': 'u-b34',
                'age': None
            }
        )
        # Tests to_dict output contradiction
        test_mdl_d = City()
        self.assertIn('__class__', City().to_dict())
        self.assertNotIn('__class__', City().__dict__)
        self.assertNotEqual(test_mdl_d.to_dict(), test_mdl_d.__dict__)
        self.assertNotEqual(
            test_mdl_d.to_dict()['__class__'],
            test_mdl_d.__class__
        )
        # Tests to_dict with arg
        with self.assertRaises(TypeError):
            City().to_dict(None)
        with self.assertRaises(TypeError):
            City().to_dict(City())
        with self.assertRaises(TypeError):
            City().to_dict(45)

    def tearDown(self):
        """Deconstructs this test class.
        """
        super().tearDown()
        if os.path.isfile('file.json'):
            os.unlink('file.json')
