#!/usr/bin/python3
"""Defines unittests for models/state.py.

Unittest classes:
    TestStateInstantiation
    TestStateSave
    TestStateToDict
"""
import os
import unittest
from time import sleep
from datetime import datetime, timedelta
from models.state import State
import models


class TestStateInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def setUp(self):
        self.state_instance = State()

    def test_instantiates(self):
        self.assertEqual(State, type(self.state_instance))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(self.state_instance, models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(self.state_instance.id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(self.state_instance.created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(self.state_instance.updated_at))

    def test_name_is_public_class_attribute(self):
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(self.state_instance))
        self.assertNotIn("name", self.state_instance.__dict__)

    def test_unique_ids(self):
        another_state_instance = State()
        self.assertNotEqual(self.state_instance.id, another_state_instance.id)

    def test_different_created_at(self):
        sleep_duration = timedelta(milliseconds=50)
        initial_created_at = self.state_instance.created_at
        sleep(sleep_duration.total_seconds())
        new_state_instance = State()
        self.assertLess(initial_created_at, new_state_instance.created_at)

    def test_different_updated_at(self):
        sleep_duration = timedelta(milliseconds=50)
        initial_updated_at = self.state_instance.updated_at
        sleep(sleep_duration.total_seconds())
        new_state_instance = State()
        self.assertLess(initial_updated_at, new_state_instance.updated_at)

    def test_string_representation(self):
        current_datetime = datetime.today()
        self.state_instance.id = "123456"
        self.state_instance.created_at = current_datetime
        self.state_instance.updated_at = current_datetime
        datetime_repr = repr(current_datetime)
        state_str = str(self.state_instance)
        self.assertIn("[State] (123456)", state_str)
        self.assertIn("'id': '123456'", state_str)
        self.assertIn("'created_at': " + datetime_repr, state_str)
        self.assertIn("'updated_at': " + datetime_repr, state_str)

    def test_unused_args(self):
        self.assertNotIn(None, self.state_instance.__dict__.values())

    def test_instantiation_with_kwargs(self):
        current_datetime = datetime.today()
        datetime_iso = current_datetime.isoformat()
        state_instance = State(id="345", created_at=datetime_iso, updated_at=datetime_iso)
        self.assertEqual(state_instance.id, "345")
        self.assertEqual(state_instance.created_at, current_datetime)
        self.assertEqual(state_instance.updated_at, current_datetime)

    def test_instantiation_with_none_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestStateSave(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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
        self.state_instance = State()

    def test_single_save(self):
        initial_updated_at = self.state_instance.updated_at
        sleep(0.05)
        self.state_instance.save()
        self.assertLess(initial_updated_at, self.state_instance.updated_at)

    def test_multiple_saves(self):
        initial_updated_at = self.state_instance.updated_at
        sleep(0.05)
        self.state_instance.save()
        intermediate_updated_at = self.state_instance.updated_at
        self.assertLess(initial_updated_at, intermediate_updated_at)
        sleep(0.05)
        self.state_instance.save()
        self.assertLess(intermediate_updated_at, self.state_instance.updated_at)

    def test_save_with_argument(self):
        with self.assertRaises(TypeError):
            self.state_instance.save(None)

    def test_save_updates_file(self):
        self.state_instance.save()
        state_id = "State." + self.state_instance.id
        with open("file.json", "r") as file:
            self.assertIn(state_id, file.read())


class TestStateToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def setUp(self):
        self.state_instance = State()

    def test_to_dict_type(self):
        self.assertTrue(dict, type(self.state_instance.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        state_dict = self.state_instance.to_dict()
        self.assertIn("id", state_dict)
        self.assertIn("created_at", state_dict)
        self.assertIn("updated_at", state_dict)
        self.assertIn("__class__", state_dict)

    def test_to_dict_contains_added_attributes(self):
        self.state_instance.middle_name = "AUSchool"
        self.state_instance.my_number = 98
        self.assertEqual("AUSchool", self.state_instance.middle_name)
        state_dict = self.state_instance.to_dict()
        self.assertIn("my_number", state_dict)

    def test_to_dict_datetime_attributes_are_strs(self):
        state_dict = self.state_instance.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        current_datetime = datetime.today()
        self.state_instance.id = "123456"
        self.state_instance.created_at = current_datetime
        self.state_instance.updated_at = current_datetime
        expected_dict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': current_datetime.isoformat(),
            'updated_at': current_datetime.isoformat(),
        }
        self.assertDictEqual(self.state_instance.to_dict(), expected_dict)

    def test_to_dict_differ_from_instance_dict(self):
        self.assertNotEqual(self.state_instance.to_dict(), self.state_instance.__dict__)

    def test_to_dict_with_argument(self):
        with self.assertRaises(TypeError):
            self.state_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()

