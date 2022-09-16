#!/usr/bin/python3
"""A unit test module for the place model.
"""
from models.base_model import BaseModel
from models.place import Place
import os
import unittest
from datetime import datetime


class TestPlace(unittest.TestCase):
    """Represents the test class for the Place class.
    """

    def test_init(self):
        """Tests the initialization of the Place class.
        """
        self.assertIsInstance(Place(), BaseModel)
        self.assertTrue(hasattr(Place, 'city_id'))
        self.assertTrue(hasattr(Place, 'user_id'))
        self.assertTrue(hasattr(Place, 'name'))
        self.assertTrue(hasattr(Place, 'description'))
        self.assertTrue(hasattr(Place, 'number_rooms'))
        self.assertTrue(hasattr(Place, 'number_bathrooms'))
        self.assertTrue(hasattr(Place, 'max_guest'))
        self.assertTrue(hasattr(Place, 'price_by_night'))
        self.assertTrue(hasattr(Place, 'latitude'))
        self.assertTrue(hasattr(Place, 'longitude'))
        self.assertTrue(hasattr(Place, 'amenity_ids'))
        self.assertIsInstance(Place.city_id, str)
        self.assertIsInstance(Place.user_id, str)
        self.assertIsInstance(Place.name, str)
        self.assertIsInstance(Place.description, str)
        self.assertIsInstance(Place.number_rooms, int)
        self.assertIsInstance(Place.number_bathrooms, int)
        self.assertIsInstance(Place.max_guest, int)
        self.assertIsInstance(Place.price_by_night, int)
        self.assertIsInstance(Place.latitude, float)
        self.assertIsInstance(Place.longitude, float)
        self.assertIsInstance(Place.amenity_ids, list)
        self.assertEqual(Place().city_id, '')
        self.assertEqual(Place().user_id, '')
        self.assertEqual(Place().name, '')
        self.assertEqual(Place().description, '')
        self.assertEqual(Place().number_rooms, 0)
        self.assertEqual(Place().number_bathrooms, 0)
        self.assertEqual(Place().max_guest, 0)
        self.assertEqual(Place().price_by_night, 0)
        self.assertEqual(Place().latitude, 0.0)
        self.assertEqual(Place().longitude, 0.0)
        self.assertEqual(Place().amenity_ids, [])
        self.assertEqual(Place('p-d62').city_id, '')
        self.assertEqual(Place('u-a98').user_id, '')
        self.assertEqual(Place('Beach').name, '')
        self.assertEqual(Place('Classic').description, '')
        self.assertEqual(Place(3).number_rooms, 0)
        self.assertEqual(Place(4).number_bathrooms, 0)
        self.assertEqual(Place(8).max_guest, 0)
        self.assertEqual(Place(120).price_by_night, 0)
        self.assertEqual(Place(12.3).latitude, 0.0)
        self.assertEqual(Place(56.8).longitude, 0.0)
        self.assertEqual(Place(['a-f3', 'a-c5']).amenity_ids, [])
        self.assertEqual(Place(city_id='p-d62').city_id, 'p-d62')
        self.assertEqual(Place(user_id='u-a98').user_id, 'u-a98')
        self.assertEqual(Place(name='Meadow').name, 'Meadow')
        self.assertEqual(Place(description='Calm').description, 'Calm')
        self.assertEqual(Place(number_rooms=3).number_rooms, 3)
        self.assertEqual(Place(number_bathrooms=4).number_bathrooms, 4)
        self.assertEqual(Place(max_guest=8).max_guest, 8)
        self.assertEqual(Place(price_by_night=120).price_by_night, 120)
        self.assertEqual(Place(latitude=12.3).latitude, 12.3)
        self.assertEqual(Place(longitude=56.8).longitude, 56.8)
        self.assertEqual(Place(amenity_ids=['a-f3']).amenity_ids, ['a-f3'])
        self.assertEqual(Place('p-87', city_id='p-d62').city_id, 'p-d62')
        self.assertEqual(Place('u-13', user_id='u-a98').user_id, 'u-a98')
        self.assertEqual(Place('Accra', name='Meadow').name, 'Meadow')
        self.assertEqual(Place('eh', description='Calm').description, 'Calm')
        self.assertEqual(Place(8, number_rooms=4).number_rooms, 4)
        self.assertEqual(Place(13, number_bathrooms=3).number_bathrooms, 3)
        self.assertEqual(Place(6, max_guest=3).max_guest, 3)
        self.assertEqual(Place(350, price_by_night=150).price_by_night, 150)
        self.assertEqual(Place(34.7, latitude=32.1).latitude, 32.1)
        self.assertEqual(Place(18.7, longitude=76.8).longitude, 76.8)
        self.assertEqual(Place([], amenity_ids=['a-f3']).amenity_ids, ['a-f3'])

    def test_str(self):
        """Tests the __str__ representation function of the Place class.
        """
        datetime_now = datetime.today()
        datetime_repr = repr(datetime_now)
        test_mdl = Place()
        test_mdl.id = '012345'
        test_mdl.created_at = test_mdl.updated_at = datetime_now
        test_mdl_str = str(test_mdl)
        self.assertIn("[Place] (012345)", test_mdl_str)
        self.assertIn("'id': '012345'", test_mdl_str)
        self.assertIn("'created_at': " + datetime_repr, test_mdl_str)
        self.assertIn("'updated_at': " + datetime_repr, test_mdl_str)
        self.assertIn("'id': ", str(Place()))
        self.assertIn("'created_at': ", str(Place()))
        self.assertIn("'updated_at': ", str(Place()))
        self.assertIn(
            "'gender': 'female'",
            str(Place(gender='female', id='m-77'))
        )
        self.assertNotIn(
            "'created_at': ",
            str(Place(gender='female', id='u-88'))
        )
        self.assertNotIn(
            "'updated_at': ",
            str(Place(gender='female', id='u-55'))
        )
        self.assertRegex(
            str(Place()),
            r'\[Place\] \([0-9a-zA-Z]+(?:-[0-9a-zA-Z]+)*\) \{.+\}'
        )
        self.assertEqual(
            str(Place(id='m-345')),
            "[Place] (m-345) {'id': 'm-345'}"
        )
        self.assertEqual(
            str(Place(id=45)),
            "[Place] (45) {'id': 45}"
        )
        self.assertEqual(
            str(Place(id=None)),
            "[Place] (None) {'id': None}"
        )
        with self.assertRaises(AttributeError):
            str(Place(gender='female'))

    def test_to_dict(self):
        """Tests the to_dict function of the Place class.
        """
        # Tests if it's a dictionary
        self.assertIsInstance(Place().to_dict(), dict)
        # Tests if to_dict contains accurate keys
        self.assertIn('id', Place().to_dict())
        self.assertIn('created_at', Place().to_dict())
        self.assertIn('updated_at', Place().to_dict())
        # Tests if to_dict contains added attributes
        test_mdl = Place()
        test_mdl.firstname = 'Jungle'
        test_mdl.lastname = 'George'
        self.assertIn('firstname', test_mdl.to_dict())
        self.assertIn('lastname', test_mdl.to_dict())
        self.assertIn('firstname', Place(firstname='Jungle').to_dict())
        self.assertIn('lastname', Place(lastname='George').to_dict())
        # Tests to_dict datetime attributes if they are strings
        self.assertIsInstance(Place().to_dict()['created_at'], str)
        self.assertIsInstance(Place().to_dict()['updated_at'], str)
        # Tests to_dict output
        datetime_now = datetime.today()
        test_mdl = Place()
        test_mdl.id = '012345'
        test_mdl.created_at = test_mdl.updated_at = datetime_now
        to_dict = {
            'id': '012345',
            '__class__': 'Place',
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(test_mdl.to_dict(), to_dict)
        self.assertDictEqual(
            Place(id='u-b34', age=13).to_dict(),
            {
                '__class__': 'Place',
                'id': 'u-b34',
                'age': 13
            }
        )
        self.assertDictEqual(
            Place(id='u-b34', age=None).to_dict(),
            {
                '__class__': 'Place',
                'id': 'u-b34',
                'age': None
            }
        )
        # Tests to_dict output contradiction
        test_mdl_d = Place()
        self.assertIn('__class__', Place().to_dict())
        self.assertNotIn('__class__', Place().__dict__)
        self.assertNotEqual(test_mdl_d.to_dict(), test_mdl_d.__dict__)
        self.assertNotEqual(
            test_mdl_d.to_dict()['__class__'],
            test_mdl_d.__class__
        )
        # Tests to_dict with arg
        with self.assertRaises(TypeError):
            Place().to_dict(None)
        with self.assertRaises(TypeError):
            Place().to_dict(Place())
        with self.assertRaises(TypeError):
            Place().to_dict(45)

    def tearDown(self):
        """Deconstructs this test class.
        """
        super().tearDown()
        if os.path.isfile('file.json'):
            os.unlink('file.json')
