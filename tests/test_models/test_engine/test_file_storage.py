#!/usr/bin/python3
"""Unittest to test FileStorage class"""

import unittest
import json
import os
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """testing file storage"""

    @classmethod
    def setUpClass(cls):
        cls.usr = User()
        cls.usr.first_name = "Awe"
        cls.usr.last_name = "Ugochi"
        cls.usr.email = "aweugo@gmail.com"
        cls.storage = FileStorage()

    @classmethod
    def tearDownClass(cls):
        del cls.usr

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_all(self):
        """Test returning the dictionary of objects"""
        file_str = FileStorage()
        all_obj = file_str.all()
        self.assertIsNotNone(all_obj)
        self.assertEqual(type(all_obj), dict)
        self.assertIs(all_obj, file_str._FileStorage__objects)

    def test_new(self):
        """Test adding new objects to __object"""
        all_str = FileStorage()
        dic = all_str.all()
        rev = User()
        rev.id = 52
        rev.name = "Awe"
        all_str.new(rev)
        key = rev.__class__.__name__ + "." + str(rev.id)
        self.assertIsNotNone(dic[key])

    def test_reload(self):
        """Test reloading objects from JSON file"""
        b_m = BaseModel()
        u_r = User()
        p_l = Place()
        c_t = City()
        s_t = State()
        a_m = Amenity()
        r_v = Review()
        models.storage.new(b_m)
        models.storage.new(u_r)
        models.storage.new(p_l)
        models.storage.new(c_t)
        models.storage.new(s_t)
        models.storage.new(a_m)
        models.storage.new(r_v)
        models.storage.save()
        models.storage.reload()
        re_obj = models.storage.all()
        self.assertIn("BaseModel." + b_m.id, re_obj)
        self.assertIn("User." + u_r.id, re_obj)
        self.assertIn("Place." + p_l.id, re_obj)
        self.assertIn("City." + c_t.id, re_obj)
        self.assertIn("State." + s_t.id, re_obj)
        self.assertIn("Amenity." + a_m.id, re_obj)
        self.assertIn("Review." + r_v.id, re_obj)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)

    def test_reload_without_arg(self):
        # Since we expect FileNotFoundError not to be raised,
        # just call models.storage.reload without an assertion
        models.storage.reload()

if __name__ == "__main__":
    unittest.main()

