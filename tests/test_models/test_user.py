#!/usr/bin/python3
"""Unittest for User class"""
import unittest
import os
from models.user import User
from datetime import datetime
import time
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """Tests Cases for User class"""

    @classmethod
    def setUp(cls):
        """creates class"""
        cls.User_test = User()
        cls.User_test.email = "email"
        cls.User_test.password = "xxx"
        cls.User_test.first_name = "first"
        cls.User_test.last_name = "last"

    @classmethod
    def tearDown(self):
        """deletes test class"""
        del self.User_test
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_strings(self):
        self.assertEqual(type(self.User_test.email), str)
        self.assertEqual(type(self.User_test.password), str)
        self.assertEqual(type(self.User_test.first_name), str)
        self.assertEqual(type(self.User_test.first_name), str)

    def test_strings(self):
        """Tests strings"""

        self.assertTrue(len(User.__doc__) > 0)
        for func in dir(User):
            self.assertTrue(len(func.__doc__) > 0)

    def test_save(self):
        self.User_test.save()
        self.assertTrue(self.User_test.updated_at != self.User_test.created_at)

    def test_init(self):
        """Test Instantiation"""

        self.assertTrue(isinstance(self.User_test, User))
        self.assertTrue(issubclass(type(self.User_test), BaseModel))
        self.assertTrue('email' in self.User_test.__dict__)
        self.assertTrue('id' in self.User_test.__dict__)
        self.assertTrue('created_at' in self.User_test.__dict__)
        self.assertTrue('updated_at' in self.User_test.__dict__)
        self.assertTrue('password' in self.User_test.__dict__)
        self.assertTrue('first_name' in self.User_test.__dict__)
        self.assertTrue('last_name' in self.User_test.__dict__)

    def test_to_dict(self):
        self.assertEqual('to_dict' in dir(self.User_test), True)


if __name__ == '__main__':
    unittest.main()

