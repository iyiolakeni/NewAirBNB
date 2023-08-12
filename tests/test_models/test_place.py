#!/usr/bin/python3
"""Defines unittests for models/place.py.

Unittest classes:
    TestPlaceInstantiation
    TestPlaceSave
    TestPlaceToDict
"""
import os
import unittest
from datetime import datetime
from time import sleep
from models.place import Place
import models


class TestPlaceInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def setUp(self):
        """Set up the test environment."""
        self.place = Place()

    def tearDown(self):
        """Clean up after each test."""
        del self.place

    def test_instance_creation(self):
        """Test if a new instance of Place is created."""
        self.assertIsInstance(self.place, Place)

    def test_new_instance_stored_in_objects(self):
        """Test if a new instance is stored in objects."""
        self.assertIn(self.place, models.storage.all().values())

    def test_id_is_public_str(self):
        """Test if id is a public string attribute."""
        self.assertEqual(str, type(self.place.id))

    # Other instantiation tests...

    def test_two_places_unique_ids(self):
        """Test if two instances have unique ids."""
        place2 = Place()
        self.assertNotEqual(self.place.id, place2.id)

    # More instantiation tests...


class TestPlaceSave(unittest.TestCase):
    """Unittests for testing the save method of the Place class."""

    def setUp(self):
        """Set up the test environment."""
        self.place = Place()

    def tearDown(self):
        """Clean up after each test."""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_save_updates_timestamp(self):
        """Test if save updates the updated_at timestamp."""
        first_updated_at = self.place.updated_at
        sleep(0.05)
        self.place.save()
        self.assertLess(first_updated_at, self.place.updated_at)

    def test_save_updates_file(self):
        """Test if save updates the file with correct id."""
        self.place.save()
        pl_id = "Place." + self.place.id
        with open("file.json", "r") as f:
            self.assertIn(pl_id, f.read())

    # Other save tests...


class TestPlaceToDict(unittest.TestCase):
    """Unittests for testing the to_dict method of the Place class."""

    def setUp(self):
        """Set up the test environment."""
        self.place = Place()

    def tearDown(self):
        """Clean up after each test."""
        del self.place

    def test_to_dict_contains_correct_keys(self):
        """Test if to_dict contains the correct keys."""
        pl_dict = self.place.to_dict()
        self.assertIn("id", pl_dict)
        self.assertIn("created_at", pl_dict)
        self.assertIn("updated_at", pl_dict)
        self.assertIn("__class__", pl_dict)

    def test_to_dict_output(self):
        """Test the output of the to_dict method."""
        dt = datetime.today()
        self.place.id = "123456"
        self.place.created_at = self.place.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(self.place.to_dict(), expected_dict)

    # Other to_dict tests...


if __name__ == "__main__":
    unittest.main()

