#!/usr/bin/python3
"""Test suite for DBStorage class"""
import unittest
import os
from models import storage
from models.base_model import BaseModel
from models.user import User

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Testing DBStorage only")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    def setUp(self):
        """Set up for the tests"""
        self.storage = storage
        self.new_user = User(email="test@test.com", password="password")
        self.new_user.save()

    def tearDown(self):
        """Tear down for the tests"""
        self.storage.delete(self.new_user)
        self.storage.save()

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new(self):
        """Test that new adds an object to the database"""
        user = User(email="new@test.com", password="password")
        self.storage.new(user)
        self.storage.save()
        self.assertIn(user, self.storage.all(User).values())

    def test_save(self):
        """Test that save properly saves objects to the database"""
        self.new_user.email = "update@test.com"
        self.storage.save()
        updated_user = self.storage.all(User)[self.new_user.__class__.__name__ + '.' + self.new_user.id]
        self.assertEqual(updated_user.email, "update@test.com")

    def test_delete(self):
        """Test that delete properly deletes objects from the database"""
        self.storage.delete(self.new_user)
        self.storage.save()
        self.assertNotIn(self.new_user, self.storage.all(User).values())

    def test_reload(self):
        """Test that reload properly reloads objects from the database"""
        self.storage.reload()
        self.assertIn(self.new_user, self.storage.all(User).values())

