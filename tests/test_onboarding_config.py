"""Tests for onboarding configuration functions.

These tests verify that the onboarding tracking functions work correctly
with the database layer.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestOnboardingConfig(unittest.TestCase):
    """Test cases for onboarding configuration functions."""

    @patch('cloud.ivanbotty.database.sqlite3.get_pref')
    def test_should_show_onboarding_default_true(self, mock_get_pref):
        """Test that should_show_onboarding returns True by default."""
        mock_get_pref.return_value = True
        
        from cloud.ivanbotty.Launcher.config.config import should_show_onboarding
        
        result = should_show_onboarding()
        self.assertTrue(result)
        mock_get_pref.assert_called_once_with("show_welcome_wizard", True)

    @patch('cloud.ivanbotty.database.sqlite3.get_pref')
    def test_should_show_onboarding_false_when_completed(self, mock_get_pref):
        """Test that should_show_onboarding returns False when completed."""
        mock_get_pref.return_value = False
        
        from cloud.ivanbotty.Launcher.config.config import should_show_onboarding
        
        result = should_show_onboarding()
        self.assertFalse(result)

    @patch('cloud.ivanbotty.database.sqlite3.get_pref')
    def test_should_show_onboarding_handles_errors(self, mock_get_pref):
        """Test that should_show_onboarding handles database errors gracefully."""
        mock_get_pref.side_effect = Exception("Database error")
        
        from cloud.ivanbotty.Launcher.config.config import should_show_onboarding
        
        result = should_show_onboarding()
        self.assertTrue(result)  # Should default to True on error

    @patch('cloud.ivanbotty.database.sqlite3.set_pref')
    def test_mark_onboarding_complete(self, mock_set_pref):
        """Test that mark_onboarding_complete sets correct preferences."""
        from cloud.ivanbotty.Launcher.config.config import mark_onboarding_complete
        
        mark_onboarding_complete()
        
        # Should be called twice: once for show_welcome_wizard, once for timestamp
        self.assertEqual(mock_set_pref.call_count, 2)
        
        # First call should set show_welcome_wizard to False
        first_call = mock_set_pref.call_args_list[0]
        self.assertEqual(first_call[0][0], "show_welcome_wizard")
        self.assertEqual(first_call[0][1], False)
        
        # Second call should set onboarding_completed_at timestamp
        second_call = mock_set_pref.call_args_list[1]
        self.assertEqual(second_call[0][0], "onboarding_completed_at")
        self.assertIsInstance(second_call[0][1], str)  # Should be string timestamp

    @patch('cloud.ivanbotty.database.sqlite3.set_pref')
    def test_mark_onboarding_complete_handles_errors(self, mock_set_pref):
        """Test that mark_onboarding_complete handles database errors gracefully."""
        mock_set_pref.side_effect = Exception("Database error")
        
        from cloud.ivanbotty.Launcher.config.config import mark_onboarding_complete
        
        # Should not raise an exception
        try:
            mark_onboarding_complete()
        except Exception as e:
            self.fail(f"mark_onboarding_complete raised an exception: {e}")

    @patch('cloud.ivanbotty.database.sqlite3.set_pref')
    def test_reset_onboarding(self, mock_set_pref):
        """Test that reset_onboarding sets show_welcome_wizard to True."""
        from cloud.ivanbotty.Launcher.config.config import reset_onboarding
        
        reset_onboarding()
        
        mock_set_pref.assert_called_once_with("show_welcome_wizard", True)

    @patch('cloud.ivanbotty.database.sqlite3.set_pref')
    def test_reset_onboarding_handles_errors(self, mock_set_pref):
        """Test that reset_onboarding handles database errors gracefully."""
        mock_set_pref.side_effect = Exception("Database error")
        
        from cloud.ivanbotty.Launcher.config.config import reset_onboarding
        
        # Should not raise an exception
        try:
            reset_onboarding()
        except Exception as e:
            self.fail(f"reset_onboarding raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()
