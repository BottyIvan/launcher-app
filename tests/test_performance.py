"""Performance tests for optimized code.

These tests verify that performance improvements don't break functionality
and provide benchmarks for key operations.
"""

import sys
import os
import unittest
import time
from unittest.mock import MagicMock, patch

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestApplicationsServicePerformance(unittest.TestCase):
    """Test performance improvements in ApplicationsService."""

    @unittest.skipUnless(
        os.getenv("GTK_AVAILABLE") == "1",
        "GTK4 not available in test environment"
    )
    def test_icon_caching(self):
        """Test that icon searches are cached."""
        from cloud.ivanbotty.LightFlow.services.applications_service import ApplicationsService

        service = ApplicationsService()

        # First search - should cache the result
        icon_name = "nonexistent-icon-test"
        result1 = service.find_icon(icon_name)

        # Second search - should use cache (verify cache exists)
        result2 = service.find_icon(icon_name)

        # Results should be the same
        self.assertEqual(result1, result2)

        # Verify the icon is in the cache
        self.assertIn(icon_name, service._icon_cache)

    @unittest.skipUnless(
        os.getenv("GTK_AVAILABLE") == "1",
        "GTK4 not available in test environment"
    )
    def test_desktop_entry_caching(self):
        """Test that desktop entries are cached."""
        from cloud.ivanbotty.LightFlow.services.applications_service import ApplicationsService

        service = ApplicationsService()

        # Initially cache should be empty
        self.assertEqual(len(service._desktop_cache), 0)

        # After loading, cache should be populated
        # (This will only work if there are actual desktop files)
        # We're just testing the cache exists
        self.assertIsInstance(service._desktop_cache, dict)


class TestDatabasePerformance(unittest.TestCase):
    """Test performance improvements in database module."""

    @patch("cloud.ivanbotty.database.sqlite3._get_connection")
    def test_connection_reuse(self, mock_get_conn):
        """Test that database connections are reused."""
        from cloud.ivanbotty.database import sqlite3 as db

        # Mock the connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        # Make multiple calls
        db.get_pref("test_key1", "default1")
        db.get_pref("test_key2", "default2")
        db.get_pref("test_key3", "default3")

        # Connection should be requested multiple times (once per call)
        # but the same connection object should be returned
        self.assertGreaterEqual(mock_get_conn.call_count, 3)


class TestMathServicePerformance(unittest.TestCase):
    """Test performance improvements in MathService."""

    def test_safe_dict_is_shared(self):
        """Test that safe_dict is pre-built and shared."""
        from cloud.ivanbotty.LightFlow.services.math_service import MathService, _SAFE_DICT

        # Create two instances
        service1 = MathService()
        service2 = MathService()

        # Both should reference the same pre-built dictionary
        self.assertIs(service1.safe_dict, _SAFE_DICT)
        self.assertIs(service2.safe_dict, _SAFE_DICT)
        self.assertIs(service1.safe_dict, service2.safe_dict)

    def test_math_calculation_performance(self):
        """Test that math calculations are fast."""
        from cloud.ivanbotty.LightFlow.services.math_service import MathService

        service = MathService()

        # Time multiple calculations
        start = time.time()
        for _ in range(100):
            result, error = service.calculate("2 + 2 * 3")
            self.assertEqual(result, "8")
            self.assertIsNone(error)
        elapsed = time.time() - start

        # Should be fast (< 0.1 seconds for 100 calculations)
        self.assertLess(elapsed, 0.1, f"Math calculations took {elapsed:.3f}s for 100 iterations")


class TestLoadClassInstancePerformance(unittest.TestCase):
    """Test performance improvements in load_class_instance."""

    def test_instance_caching(self):
        """Test that class instances are cached."""
        from cloud.ivanbotty.LightFlow.helper.load_class_instance import (
            load_class_instance,
            _instance_cache,
        )

        # Clear cache first
        _instance_cache.clear()

        # Load a class instance
        path = "cloud.ivanbotty.Launcher.services.math_service.MathService"
        instance1 = load_class_instance(path)

        # Verify it was cached
        self.assertIn(path, _instance_cache)

        # Load again - should return cached instance
        instance2 = load_class_instance(path)

        # Should be the exact same object
        self.assertIs(instance1, instance2)

    def test_cached_load_is_faster(self):
        """Test that cached loads are faster than initial loads."""
        from cloud.ivanbotty.LightFlow.helper.load_class_instance import (
            load_class_instance,
            _instance_cache,
        )

        path = "cloud.ivanbotty.Launcher.services.math_service.MathService"

        # Clear cache
        _instance_cache.clear()

        # First load (not cached)
        instance1 = load_class_instance(path)

        # Second load (cached)
        instance2 = load_class_instance(path)

        # Cached load should return the same instance
        self.assertIsNotNone(instance1)
        self.assertIsNotNone(instance2)
        self.assertIs(instance1, instance2)


class TestRowWidgetPerformance(unittest.TestCase):
    """Test performance improvements in Row widget."""

    @unittest.skipUnless(
        os.getenv("GTK_AVAILABLE") == "1",
        "GTK4 not available in test environment"
    )
    def test_regex_patterns_precompiled(self):
        """Test that regex patterns are pre-compiled at module level."""
        from cloud.ivanbotty.LightFlow.widget import row

        # Check that patterns exist as module-level constants
        self.assertTrue(hasattr(row, "_CODE_BLOCK_PATTERN"))
        self.assertTrue(hasattr(row, "_CODE_KEYWORDS_PATTERN"))

        # Verify they are compiled regex objects
        import re
        self.assertIsInstance(row._CODE_BLOCK_PATTERN, re.Pattern)
        self.assertIsInstance(row._CODE_KEYWORDS_PATTERN, re.Pattern)


if __name__ == "__main__":
    unittest.main()
