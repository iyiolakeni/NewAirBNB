#!/usr/bin/python3
"""tests for class amenity"""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity

class TestAmenityFunctionality(unittest.TestCase):
    def setUp(self):
        """Set up any resources needed for the test cases."""
        pass

    def tearDown(self):
        """Clean up any resources after the test cases."""
        pass

    # Tests related to instantiation of the Amenity class
    def test_basic_instantiation(self):
        """Test basic instantiation of the Amenity class."""
        amenity = Amenity()
        self.assertEqual(Amenity, type(amenity))
        self.assertIn(amenity, models.storage.all().values())
        self.assertEqual(str, type(amenity.id))
        self.assertEqual(datetime, type(amenity.created_at))
        self.assertEqual(datetime, type(amenity.updated_at))
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amenity.__dict__)

    def test_unique_ids(self):
        """Test that two instances of Amenity have unique ids."""
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)

    def test_timestamps(self):
        """Test that created_at and updated_at timestamps are set properly."""
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.created_at, amenity2.created_at)
        self.assertLess(amenity1.updated_at, amenity2.updated_at)

    def test_str_representation(self):
        """Test the string representation of Amenity."""
        current_datetime = datetime.today()
        datetime_repr = repr(current_datetime)
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = current_datetime
        amenity_str = str(amenity)
        self.assertIn("[Amenity] (123456)", amenity_str)
        self.assertIn("'id': '123456'", amenity_str)
        self.assertIn("'created_at': " + datetime_repr, amenity_str)
        self.assertIn("'updated_at': " + datetime_repr, amenity_str)


if __name__ == "__main__":
    unittest.main()

