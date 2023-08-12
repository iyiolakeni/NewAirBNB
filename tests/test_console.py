#!/usr/bin/python3
"""Tests for the console"""
import unittest
import os
import console
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch

class TestConsole(unittest.TestCase):
    """Tests for the console functionality."""

    @classmethod
    def setUpClass(cls):
        """Setup the console instance for testing."""
        cls.console_instance = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """Teardown the console instance after testing."""
        del cls.console_instance

    def tearDown(self):
        """Delete the file after each test."""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_empty_line(self):
        """Test handling of an empty line input."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.console_instance.onecmd("")
            self.assertEqual("", output.getvalue().strip())

    def test_quit_command(self):
        """Test the functionality of the 'quit' command."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.console_instance.onecmd("quit")
            self.assertEqual("", output.getvalue().strip())

    def test_create_command(self):
        """Test the functionality of the 'create' command."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.console_instance.onecmd("create BaseModel")
            obj_id = output.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as output:
            self.console_instance.onecmd(f"show BaseModel {obj_id}")
            self.assertIn(obj_id, output.getvalue().strip())

    def test_show_command(self):
        """Test the functionality of the 'show' command."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.console_instance.onecmd("create BaseModel")
            obj_id = output.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as output:
            self.console_instance.onecmd(f"show BaseModel {obj_id}")
            self.assertIn(obj_id, output.getvalue().strip())

    def test_destroy_command(self):
        """Test the functionality of the 'destroy' command."""
        with patch('sys.stdout', new=StringIO()) as output:
            self.console_instance.onecmd("create BaseModel")
            obj_id = output.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as output:
            self.console_instance.onecmd(f"destroy BaseModel {obj_id}")
            self.assertEqual("", output.getvalue().strip())

if __name__ == "__main__":
    unittest.main()

