#!/usr/bin/python3
"""Unittest Models for Models/city.py """

import unittest
import os
import models
from datetime import datetime
from time import sleep
from models.city import City

class TestCityFunctionality(unittest.TestCase):
    def setUp(self):
        """Set up any resources needed for the test cases."""
        pass

    def tearDown(self):
        """Clean up any resources after the test cases."""
        pass

    # Tests related to instantiation of the City class
    def test_instantiation(self):
        """Test basic instantiation of the City class."""
        city = City()
        self.assertEqual(City, type(city))
        self.assertEqual(str, type(city.id))
        self.assertEqual(datetime, type(city.created_at))
        self.assertEqual(datetime, type(city.updated_at))
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(city))
        self.assertNotIn("state_id", city.__dict__)
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(city))
        self.assertNotIn("name", city.__dict__)

    def test_unique_ids(self):
        """Test that two instances of City have unique ids."""
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_timestamps(self):
        """Test that created_at and updated_at timestamps are set properly."""
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)
        self.assertLess(city1.updated_at, city2.updated_at)

    def test_str_representation(self):
        """Test the string representation of City."""
        dt = datetime.today()
        dt_repr = repr(dt)
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = dt
        city_str = str(city)
        self.assertIn("[City] (123456)", city_str)
        self.assertIn("'id': '123456'", city_str)
        self.assertIn("'created_at': " + dt_repr, city_str)
        self.assertIn("'updated_at': " + dt_repr, city_str)

    # ... Add more tests for other functionalities ...

class TestCitySave(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        self.assertLess(first_updated_at, city.updated_at)

    def test_two_saves(self):
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        second_updated_at = city.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city.save()
        self.assertLess(second_updated_at, city.updated_at)

    def test_save_with_arg(self):
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    def test_save_updates_file(self):
        city = City()
        city.save()
        city_id = "City." + city.id
        with open("file.json", "r") as f:
            self.assertIn(city_id, f.read())

class TestCityToDict(unittest.TestCase):
    def test_to_dict_type(self):
        city = City()
        self.assertIsInstance(city.to_dict(), dict)

    def test_to_dict_contains_correct_keys(self):
        city = City()
        self.assertIn("id", city.to_dict())
        self.assertIn("created_at", city.to_dict())
        self.assertIn("updated_at", city.to_dict())
        self.assertIn("__class__", city.to_dict())

    def test_to_dict_contains_added_attributes(self):
        city = City()
        city.middle_name = "AUStreet"
        city.my_number = 101
        self.assertEqual("AUStreet", city.middle_name)
        self.assertIn("my_number", city.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        city = City()
        city_dict = city.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(city.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        city = City()
        self.assertNotEqual(city.to_dict(), city.__dict__)

    def test_to_dict_with_arg(self):
        city = City()
        with self.assertRaises(TypeError):
            city.to_dict(None)

if __name__ == "__main__":
    unittest.main()

