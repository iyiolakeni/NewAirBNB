#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
    TestReview
"""
import os
import models
import unittest
from datetime import datetime, timedelta
from time import sleep
from models.review import Review


class TestReview(unittest.TestCase):
    """Unittests for Review class."""

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

    def setUp(self):
        self.review_instance = Review()

    def test_instantiation(self):
        self.assertIsInstance(self.review_instance, Review)
        self.assertIn(self.review_instance, models.storage.all().values())
        self.assertEqual(str, type(self.review_instance.id))
        self.assertEqual(datetime, type(self.review_instance.created_at))
        self.assertEqual(datetime, type(self.review_instance.updated_at))
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(self.review_instance))
        self.assertNotIn("place_id", self.review_instance.__dict__)
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(self.review_instance))
        self.assertNotIn("user_id", self.review_instance.__dict__)
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(self.review_instance))
        self.assertNotIn("text", self.review_instance.__dict__)

    def test_unique_ids_and_times(self):
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)
        self.assertLess(review1.created_at, review2.created_at)
        self.assertLess(review1.updated_at, review2.updated_at)

    def test_string_representation(self):
        current_datetime = datetime.today()
        self.review_instance.id = "123456"
        self.review_instance.created_at = self.review_instance.updated_at = current_datetime
        current_datetime_repr = repr(current_datetime)
        review_str = self.review_instance.__str__()
        self.assertIn("[Review] (123456)", review_str)
        self.assertIn("'id': '123456'", review_str)
        self.assertIn("'created_at': " + current_datetime_repr, review_str)
        self.assertIn("'updated_at': " + current_datetime_repr, review_str)

    def test_save(self):
        initial_updated_at = self.review_instance.updated_at
        self.review_instance.save()
        self.assertLess(initial_updated_at, self.review_instance.updated_at)
        review_id = "Review." + self.review_instance.id
        with open("file.json", "r") as f:
            self.assertIn(review_id, f.read())

    def assertDictSubset(self, subdict, maindict):
        for key, value in subdict.items():
            self.assertEqual(value, maindict.get(key))

    def test_to_dict(self):
        current_datetime = datetime.today()
        self.review_instance.id = "123456"
        self.review_instance.created_at = self.review_instance.updated_at = current_datetime
        expected_dict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': current_datetime.isoformat(),
            'updated_at': current_datetime.isoformat(),
        }
        review_dict = self.review_instance.to_dict()
        self.assertIsInstance(review_dict, dict)
        self.assertDictSubset(expected_dict, review_dict)
        self.assertNotEqual(review_dict, self.review_instance.__dict__)

if __name__ == "__main__":
    unittest.main()
