import unittest
from components.file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    def test_validate_file(self):
        self.assertTrue(FileHandler.validate_file("test.sql"))  # Replace with an actual valid path during testing
        self.assertFalse(FileHandler.validate_file("invalid.txt"))
        self.assertFalse(FileHandler.validate_file("nonexistent.sql"))
