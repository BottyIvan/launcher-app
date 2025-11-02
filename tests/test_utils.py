"""Smoke tests for utility modules.

These tests verify that the basic utility functions can be imported
and executed without errors.
"""
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestAppInitUtils(unittest.TestCase):
    """Test cases for app initialization utilities."""

    def test_import_app_init_module(self):
        """Test that the app_init module can be imported."""
        try:
            from cloud.ivanbotty.utils import app_init
            self.assertIsNotNone(app_init)
        except ImportError as e:
            self.fail(f"Failed to import app_init module: {e}")

    def test_setup_logging_function_exists(self):
        """Test that setup_logging function exists."""
        from cloud.ivanbotty.utils.app_init import setup_logging
        self.assertTrue(callable(setup_logging))

    def test_setup_logging_basic(self):
        """Test basic logging setup."""
        from cloud.ivanbotty.utils.app_init import setup_logging
        logger = setup_logging()
        self.assertIsNotNone(logger)

    @patch("cloud.ivanbotty.utils.app_init.GTK_AVAILABLE", True)
    @patch("cloud.ivanbotty.utils.app_init.find_resource_file")
    def test_load_resources_success(self, mock_find):
        """Test successful resource loading."""
        # Need to re-import after patching
        import importlib
        import cloud.ivanbotty.utils.app_init as app_init_module

        # Mock the Gio module
        with patch.object(app_init_module, "Gio") as mock_gio:
            mock_resource = MagicMock()
            mock_gio.Resource.load.return_value = mock_resource
            
            # Mock finding the resource file
            mock_find.return_value = "/fake/path/to/resources.gresource"

            result = app_init_module.load_resources()
            self.assertTrue(result)
            mock_find.assert_called_once()
            mock_gio.Resource.load.assert_called_once_with("/fake/path/to/resources.gresource")
            mock_gio.resources_register.assert_called_once_with(mock_resource)

    @patch("cloud.ivanbotty.utils.app_init.find_resource_file")
    def test_load_resources_not_found(self, mock_find):
        """Test resource loading when resource file is not found."""
        from cloud.ivanbotty.utils.app_init import load_resources

        # Mock resource file not found
        mock_find.return_value = None

        result = load_resources()
        self.assertFalse(result)

    @patch("cloud.ivanbotty.database.sqlite3.init_db")
    def test_initialize_database_success(self, mock_init_db):
        """Test successful database initialization."""
        from cloud.ivanbotty.utils.app_init import initialize_database

        result = initialize_database()
        self.assertTrue(result)
        mock_init_db.assert_called_once()

    @patch("cloud.ivanbotty.database.sqlite3.init_db")
    def test_initialize_database_failure(self, mock_init_db):
        """Test database initialization failure."""
        from cloud.ivanbotty.utils.app_init import initialize_database

        # Mock database initialization failure
        mock_init_db.side_effect = Exception("Database error")

        result = initialize_database()
        self.assertFalse(result)


class TestCommonUtils(unittest.TestCase):
    """Test cases for common utilities."""

    def test_import_common_module(self):
        """Test that the common module can be imported."""
        try:
            from cloud.ivanbotty import common
            self.assertIsNotNone(common)
        except ImportError as e:
            self.fail(f"Failed to import common module: {e}")

    def test_find_resource_file_function_exists(self):
        """Test that find_resource_file function exists."""
        from cloud.ivanbotty.common import find_resource_file
        self.assertTrue(callable(find_resource_file))

    def test_resource_constants_exist(self):
        """Test that resource constants are defined."""
        from cloud.ivanbotty.common import PKGDATADIR, RESOURCE_SUBDIR, RESOURCE_FILE
        self.assertIsNotNone(PKGDATADIR)
        self.assertIsNotNone(RESOURCE_SUBDIR)
        self.assertIsNotNone(RESOURCE_FILE)


class TestDatabaseModule(unittest.TestCase):
    """Test cases for database module."""

    def test_import_database_module(self):
        """Test that the database module can be imported."""
        try:
            from cloud.ivanbotty.database import sqlite3 as db
            self.assertIsNotNone(db)
        except ImportError as e:
            self.fail(f"Failed to import database module: {e}")

    def test_database_functions_exist(self):
        """Test that database functions exist."""
        from cloud.ivanbotty.database import sqlite3 as db
        self.assertTrue(callable(db.init_db))
        self.assertTrue(callable(db.set_pref))
        self.assertTrue(callable(db.get_pref))
        self.assertTrue(callable(db.get_extension))
        self.assertTrue(callable(db.set_extension_enabled))
        self.assertTrue(callable(db.get_extensions))
        self.assertTrue(callable(db.set_api_key))
        self.assertTrue(callable(db.get_api_key))


if __name__ == "__main__":
    unittest.main()
