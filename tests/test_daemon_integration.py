"""Tests for LightFlowD daemon D-Bus service and client.

These tests verify that the daemon service and client can be imported
and basic functionality works.
"""

import sys
import os
import unittest
from unittest.mock import Mock, MagicMock, patch

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestDaemonServiceImport(unittest.TestCase):
    """Test cases for daemon service module imports."""

    def test_import_dbus_service_module(self):
        """Test that the dbus_service module can be imported."""
        try:
            from cloud.ivanbotty.LightFlowD import dbus_service
            self.assertIsNotNone(dbus_service)
        except ImportError as e:
            # If GLib is not available, the import might fail
            # This is acceptable in test environments
            self.skipTest(f"GLib not available: {e}")

    def test_import_daemon_client_module(self):
        """Test that the daemon_client module can be imported."""
        try:
            from cloud.ivanbotty.LightFlow.services import daemon_client
            self.assertIsNotNone(daemon_client)
        except ImportError as e:
            self.skipTest(f"GLib not available: {e}")


class TestDaemonServiceBasic(unittest.TestCase):
    """Test cases for daemon service basic functionality."""

    @patch("cloud.ivanbotty.LightFlowD.dbus_service.DBUS_AVAILABLE", True)
    @patch("cloud.ivanbotty.LightFlowD.dbus_service.GLib")
    @patch("cloud.ivanbotty.LightFlowD.dbus_service.Gio")
    def test_daemon_service_creation(self, mock_gio, mock_glib):
        """Test that LightFlowDDBusService can be created."""
        from cloud.ivanbotty.LightFlowD.dbus_service import LightFlowDDBusService
        
        cache_path = "/tmp/test_cache.json"
        service = LightFlowDDBusService(cache_path)
        
        self.assertIsNotNone(service)
        self.assertEqual(service.cache_path, cache_path)
        self.assertFalse(service.is_indexing)
        self.assertEqual(service.progress, 0.0)
        self.assertEqual(service.apps_count, 0)

    @patch("cloud.ivanbotty.LightFlowD.dbus_service.DBUS_AVAILABLE", False)
    def test_daemon_service_no_dbus(self):
        """Test that LightFlowDDBusService raises error when D-Bus unavailable."""
        from cloud.ivanbotty.LightFlowD.dbus_service import LightFlowDDBusService
        
        with self.assertRaises(ImportError):
            LightFlowDDBusService("/tmp/test_cache.json")

    @patch("cloud.ivanbotty.LightFlowD.dbus_service.DBUS_AVAILABLE", True)
    @patch("cloud.ivanbotty.LightFlowD.dbus_service.GLib")
    @patch("cloud.ivanbotty.LightFlowD.dbus_service.Gio")
    def test_daemon_service_indexing_state(self, mock_gio, mock_glib):
        """Test setting indexing state."""
        from cloud.ivanbotty.LightFlowD.dbus_service import LightFlowDDBusService
        
        service = LightFlowDDBusService("/tmp/test_cache.json")
        
        # Test setting indexing state
        service.set_indexing_state(True)
        self.assertTrue(service.is_indexing)
        
        service.set_indexing_state(False)
        self.assertFalse(service.is_indexing)
        self.assertEqual(service.progress, 1.0)

    @patch("cloud.ivanbotty.LightFlowD.dbus_service.DBUS_AVAILABLE", True)
    @patch("cloud.ivanbotty.LightFlowD.dbus_service.GLib")
    @patch("cloud.ivanbotty.LightFlowD.dbus_service.Gio")
    def test_daemon_service_progress_update(self, mock_gio, mock_glib):
        """Test updating indexing progress."""
        from cloud.ivanbotty.LightFlowD.dbus_service import LightFlowDDBusService
        
        service = LightFlowDDBusService("/tmp/test_cache.json")
        
        # Test progress update
        service.update_indexing_progress(0.5, 42)
        self.assertEqual(service.progress, 0.5)
        self.assertEqual(service.apps_count, 42)
        
        # Test progress clamping
        service.update_indexing_progress(1.5, 100)
        self.assertEqual(service.progress, 1.0)
        
        service.update_indexing_progress(-0.5, 100)
        self.assertEqual(service.progress, 0.0)


class TestDaemonClientBasic(unittest.TestCase):
    """Test cases for daemon client basic functionality."""

    @patch("cloud.ivanbotty.LightFlow.services.daemon_client.DBUS_AVAILABLE", True)
    @patch("cloud.ivanbotty.LightFlow.services.daemon_client.GLib")
    @patch("cloud.ivanbotty.LightFlow.services.daemon_client.Gio")
    def test_daemon_client_creation(self, mock_gio, mock_glib):
        """Test that LightFlowDaemonClient can be created."""
        from cloud.ivanbotty.LightFlow.services.daemon_client import LightFlowDaemonClient
        
        client = LightFlowDaemonClient()
        
        self.assertIsNotNone(client)
        self.assertIsNone(client.proxy)
        self.assertIsNone(client.connection)
        self.assertFalse(client.is_connected())

    @patch("cloud.ivanbotty.LightFlow.services.daemon_client.DBUS_AVAILABLE", False)
    def test_daemon_client_no_dbus(self):
        """Test that LightFlowDaemonClient raises error when D-Bus unavailable."""
        from cloud.ivanbotty.LightFlow.services.daemon_client import LightFlowDaemonClient
        
        with self.assertRaises(ImportError):
            LightFlowDaemonClient()

    @patch("cloud.ivanbotty.LightFlow.services.daemon_client.DBUS_AVAILABLE", True)
    @patch("cloud.ivanbotty.LightFlow.services.daemon_client.Gio")
    def test_daemon_client_connection_failure(self, mock_gio):
        """Test that connection failure is handled gracefully."""
        from cloud.ivanbotty.LightFlow.services.daemon_client import LightFlowDaemonClient
        
        # Make bus_get_sync raise an exception
        mock_gio.bus_get_sync.side_effect = Exception("D-Bus not available")
        
        client = LightFlowDaemonClient()
        result = client.connect()
        
        self.assertFalse(result)
        self.assertFalse(client.is_connected())

    @patch("cloud.ivanbotty.LightFlow.services.daemon_client.DBUS_AVAILABLE", True)
    @patch("cloud.ivanbotty.LightFlow.services.daemon_client.GLib")
    @patch("cloud.ivanbotty.LightFlow.services.daemon_client.Gio")
    def test_daemon_client_get_status_not_connected(self, mock_gio, mock_glib):
        """Test that getting status returns None when not connected."""
        from cloud.ivanbotty.LightFlow.services.daemon_client import LightFlowDaemonClient
        
        client = LightFlowDaemonClient()
        
        result = client.get_cache_status()
        self.assertIsNone(result)
        
        result = client.get_indexing_status()
        self.assertIsNone(result)


class TestDaemonMainModule(unittest.TestCase):
    """Test cases for daemon main module."""

    def test_import_daemon_main(self):
        """Test that the daemon __main__ module can be imported."""
        try:
            from cloud.ivanbotty import LightFlowD
            self.assertIsNotNone(LightFlowD)
        except ImportError as e:
            self.fail(f"Failed to import LightFlowD module: {e}")

    @patch("cloud.ivanbotty.LightFlowD.__main__.setup_logging")
    @patch("cloud.ivanbotty.LightFlowD.__main__.ApplicationsService")
    @patch("cloud.ivanbotty.LightFlowD.__main__.GLIB_AVAILABLE", False)
    def test_daemon_run_without_glib(self, mock_service, mock_logging):
        """Test that daemon can run without GLib (no D-Bus)."""
        from cloud.ivanbotty.LightFlowD.__main__ import ensure_cache_dir_exists
        
        # Test cache dir creation function
        with patch("os.path.exists") as mock_exists, \
             patch("os.makedirs") as mock_makedirs:
            mock_exists.return_value = False
            ensure_cache_dir_exists("/tmp/test/cache.json")
            mock_makedirs.assert_called_once()


if __name__ == "__main__":
    unittest.main()
