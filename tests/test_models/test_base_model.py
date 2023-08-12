#!/usr/bin/python3
"""Unitests for testing the BaseModels"""
import unittest
import os
from models.base_model import BaseModel
import time
from datetime import datetime


class TestBaseModel(unittest.TestCase):
    """tests for basemodel"""
    @classmethod
    def setUpClass(self):
        """sets up test"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        """ tears down"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_3_instantiation(self):
        """Tests instantiation of BaseModel class."""

        bm = BaseModel()
        bc = "<class 'models.base_model.BaseModel'>"
        self.assertEqual(str(type(bm)), bc)
        self.assertIsInstance(bm, BaseModel)
        self.assertTrue(issubclass(type(bm), BaseModel))

    def test_check_functions(self):
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)

    def test_attribute_basemodel(self):
        self.assertTrue(hasattr(BaseModel, "__init__"))
        self.assertTrue(hasattr(BaseModel, "save"))
        self.assertTrue(hasattr(BaseModel, "to_dict"))

    def test_init_without_args(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_init_with_args(self):
        """Test with arguments"""
        dt = datetime.now()
        dt_iso = dt.isoformat()
        bm = BaseModel("16", id="567", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "567")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_save(self):
        """Test Save"""
        bm = BaseModel()
        time.sleep(0.5)
        first_save = bm.updated_at
        bm.save()
        self.assertLess(first_save, bm.updated_at)

    def test_to_dict(self):
        bm = BaseModel()
        copy = bm.to_dict()

        self.assertIsInstance(copy, dict)
        self.assertEqual(copy['__class__'], type(bm).__name__)
        self.assertTrue('id' in copy)
        self.assertTrue('created_at' in copy)
        self.assertTrue('updated_at' in copy)

    def test_str_representation(self):
        """Test str"""
        dt = datetime.now()
        dt_rep = repr(dt)
        b = BaseModel()
        b.id = "765432"
        b.created_at = b.updated_at = dt
        bstr = b.__str__()
        self.assertIn("[BaseModel] (765432)", bstr)
        self.assertIn("'id': '765432'", bstr)
        self.assertIn("'created_at': " + dt_rep, bstr)
        self.assertIn("'updated_at': " + dt_rep, bstr)


if __name__ == "__main__":
    unittest.main()

