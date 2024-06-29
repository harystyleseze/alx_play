#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py."""
import unittest
from models.base_model import BaseModel
from models.state import State
from models.engine.file_storage import FileStorage
import os

class TestFileStorage(unittest.TestCase):
    """Unittests for testing the FileStorage class."""

    def setUp(self):
        """Set up test methods."""
        self.storage = FileStorage()
        self.state = State(name="California")
        self.state.save()
        self.key = f"State.{self.state.id}"

    def tearDown(self):
        """Tear down test methods."""
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_delete_method(self):
        """Test the delete method of FileStorage"""
        self.storage.new(self.state)
        self.storage.save()
        self.assertIn(self.key, self.storage.all())
        self.storage.delete(self.state)
        self.assertNotIn(self.key, self.storage.all())
        self.storage.delete(None)  # should not raise any exception

    def test_all_method(self):
        """Test the all method with and without class filtering"""
        self.storage.new(self.state)
        self.storage.save()
        self.assertIn(self.key, self.storage.all(State))
        self.assertNotIn(self.key, self.storage.all(BaseModel))
        self.assertIn(self.key, self.storage.all())

if __name__ == "__main__":
    unittest.main()

