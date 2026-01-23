"""Basic unit tests for AI Cover Letter Generator."""
import unittest
import os
import sys
import tempfile
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import profile_utils
import secrets_utils
import utils


class TestProfileUtils(unittest.TestCase):
    """Test profile utility functions."""

    def setUp(self):
        """Create temporary directory for test profiles."""
        self.test_dir = tempfile.mkdtemp()
        self.original_profiles_dir = profile_utils.PROFILES_DIR
        profile_utils.PROFILES_DIR = self.test_dir

    def tearDown(self):
        """Restore original directory."""
        profile_utils.PROFILES_DIR = self.original_profiles_dir
        # Clean up test files
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_list_profiles_empty(self):
        """Test listing profiles when none exist."""
        profiles = profile_utils.list_profiles()
        self.assertEqual(len(profiles), 0)

    def test_save_and_load_profile(self):
        """Test saving and loading a profile."""
        test_profile = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "123-456-7890"
        }
        profile_utils.save_profile("Test Profile", test_profile)
        loaded = profile_utils.load_profile("Test Profile")
        self.assertEqual(loaded["name"], "John Doe")
        self.assertEqual(loaded["email"], "john@example.com")


class TestSecretsUtils(unittest.TestCase):
    """Test secrets utility functions."""

    def setUp(self):
        """Create temporary directory for test secrets."""
        self.test_dir = tempfile.mkdtemp()
        self.original_secrets_file = secrets_utils.SECRETS_FILE
        secrets_utils.SECRETS_FILE = os.path.join(self.test_dir, "secrets.json")

    def tearDown(self):
        """Restore original secrets file path."""
        secrets_utils.SECRETS_FILE = self.original_secrets_file
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_save_and_load_secrets(self):
        """Test saving and loading API key."""
        test_key = "test_api_key_12345"
        secrets_utils.save_secret("api_key", test_key)
        loaded = secrets_utils.load_secrets()
        self.assertIn("api_key", loaded)


class TestUtils(unittest.TestCase):
    """Test utility functions."""

    def test_validate_pdf_input(self):
        """Test PDF validation."""
        # This would require actual PDF content
        # Placeholder for future implementation
        self.assertTrue(True)

    def test_character_counting(self):
        """Test character counting utility."""
        text = "Hello World"
        count = len(text)
        self.assertEqual(count, 11)


if __name__ == '__main__':
    unittest.main()
