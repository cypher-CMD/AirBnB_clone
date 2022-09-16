#!/usr/bin/python3
"""Unit test module for the user model."""
import unittest
from models.base_model import BaseModel
from models.user import User
import os
from datetime import datetime


class TestUser(unittest.TestCase):
    """Test class for the User class."""

    def test_init(self):
        """Tests the initialization of the User class"""
        self.assertIsInstance(User(), BaseModel)
        self.assertTrue(hasattr(User, 'first_name'))
        self.assertTrue(hasattr(User, 'last_name'))
        self.assertTrue(hasattr(User, 'email'))
        self.assertTrue(hasattr(User, 'password'))
        self.assertIsInstance(User.first_name, str)
        self.assertIsInstance(User.last_name, str)
        self.assertIsInstance(User.email, str)
        self.assertIsInstance(User.password, str)
        self.assertEqual(User().first_name, '')
        self.assertEqual(User().last_name, '')
        self.assertEqual(User().email, '')
        self.assertEqual(User().password, '')
        self.assertEqual(User('Ben').first_name, '')
        self.assertEqual(User('Pardon').last_name, '')
        self.assertEqual(User('bp@ymail.com').email, '')
        self.assertEqual(User('password123').password, '')
        self.assertEqual(User(first_name='Michael').first_name, 'Michael')
        self.assertEqual(User(last_name='Murphy').last_name, 'Murphy')
        self.assertEqual(User(email='mm@ymail.com').email, 'mm@ymail.com')
        self.assertEqual(User(password='12345').password, '12345')
        self.assertEqual(User('Steph', first_name='Simi').first_name, 'Simi')
        self.assertEqual(User('Eric', last_name='Castel').last_name, 'Castel')
        self.assertEqual(User('mo', email='n@rmail.com').email, 'n@rmail.com')
        self.assertEqual(User('12345', password='Nami').password, 'Nami')

    def test_str(self):
        """Tests the __str__ representation functionfor user class.
        """
        datetime_now = datetime.today()
        datetime_repr = repr(datetime_now)
        test_mdl = User()
        test_mdl.id = '012345'
        test_mdl.created_at = test_mdl.updated_at = datetime_now
        test_mdl_str = str(test_mdl)
        self.assertIn("[User] (012345)", test_mdl_str)
        self.assertIn("'id': '012345'", test_mdl_str)
        self.assertIn("'created_at': " + datetime_repr, test_mdl_str)
        self.assertIn("'updated_at': " + datetime_repr, test_mdl_str)
        self.assertIn("'id': ", str(User()))
        self.assertIn("'created_at': ", str(User()))
        self.assertIn("'updated_at': ", str(User()))
        self.assertIn(
            "'gender': 'female'",
            str(User(gender='female', id='m-77'))
        )
        self.assertNotIn(
            "'created_at': ",
            str(User(gender='female', id='u-88'))
        )
        self.assertNotIn(
            "'updated_at': ",
            str(User(gender='female', id='u-55'))
        )
        self.assertRegex(
            str(User()),
            r'\[User\] \([0-9a-zA-Z]+(?:-[0-9a-zA-Z]+)*\) \{.+\}'
        )
        self.assertEqual(
            str(User(id='m-345')),
            "[User] (m-345) {'id': 'm-345'}"
        )
        self.assertEqual(
            str(User(id=45)),
            "[User] (45) {'id': 45}"
        )
        self.assertEqual(
            str(User(id=None)),
            "[User] (None) {'id': None}"
        )
        with self.assertRaises(AttributeError):
            str(User(gender='female'))

    def test_to_dict(self):
        """Tests the to_dict function of the User class.
        """
        # Tests if it's a dictionary
        self.assertIsInstance(User().to_dict(), dict)
        # Tests if to_dict contains accurate keys
        self.assertIn('id', User().to_dict())
        self.assertIn('created_at', User().to_dict())
        self.assertIn('updated_at', User().to_dict())
        # Tests if to_dict contains added attributes
        test_mdl = User()
        test_mdl.firstname = 'George'
        test_mdl.lastname = 'Jungle'
        self.assertIn('firstname', test_mdl.to_dict())
        self.assertIn('lastname', test_mdl.to_dict())
        self.assertIn('firstname', User(firstname='George').to_dict())
        self.assertIn('lastname', User(lastname='Jungle').to_dict())
        # Tests to_dict datetime attributes if they are strings
        self.assertIsInstance(User().to_dict()['created_at'], str)
        self.assertIsInstance(User().to_dict()['updated_at'], str)
        # Tests to_dict output
        datetime_now = datetime.today()
        test_mdl = User()
        test_mdl.id = '012345'
        test_mdl.created_at = test_mdl.updated_at = datetime_now
        to_dict = {
            'id': '012345',
            '__class__': 'User',
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(test_mdl.to_dict(), to_dict)
        self.assertDictEqual(
            User(id='u-b34', age=13).to_dict(),
            {
                '__class__': 'User',
                'id': 'u-b34',
                'age': 13
            }
        )
        self.assertDictEqual(
            User(id='u-b34', age=None).to_dict(),
            {
                '__class__': 'User',
                'id': 'u-b34',
                'age': None
            }
        )
        # Tests to_dict output contradiction
        test_mdl_d = User()
        self.assertIn('__class__', User().to_dict())
        self.assertNotIn('__class__', User().__dict__)
        self.assertNotEqual(test_mdl_d.to_dict(), test_mdl_d.__dict__)
        self.assertNotEqual(
            test_mdl_d.to_dict()['__class__'],
            test_mdl_d.__class__
        )
        # Tests to_dict with arg
        with self.assertRaises(TypeError):
            User().to_dict(None)
        with self.assertRaises(TypeError):
            User().to_dict(User())
        with self.assertRaises(TypeError):
            User().to_dict(45)

    def tearDown(self):
        """Deconstructs this test class.
        """
        super().tearDown()
        if os.path.isfile('file.json'):
            os.unlink('file.json')
