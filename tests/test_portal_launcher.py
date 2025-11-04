"""Unit tests for the PortalLauncher class.

These tests verify the application launching functionality with mocked
D-Bus and system commands.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock, Mock, PropertyMock, call
from gi.repository import GLib

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestPortalLauncher(unittest.TestCase):
    """Test cases for the PortalLauncher class."""

    def test_import_portal_launcher(self):
        """Test that PortalLauncher can be imported."""
        try:
            from cloud.ivanbotty.Launcher.helper.portal_launcher import PortalLauncher

            self.assertIsNotNone(PortalLauncher)
        except ImportError as e:
            self.fail(f"Failed to import PortalLauncher: {e}")

    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.Gio.bus_get_sync')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.Gio.DBusProxy.new_sync')
    def test_portal_launcher_initialization_success(self, mock_proxy_new, mock_bus_get):
        """Test successful portal initialization."""
        from cloud.ivanbotty.Launcher.helper.portal_launcher import PortalLauncher

        # Mock the bus and proxy
        mock_bus = MagicMock()
        mock_proxy = MagicMock()
        mock_bus_get.return_value = mock_bus
        mock_proxy_new.return_value = mock_proxy
        
        # Mock version property
        mock_version = MagicMock()
        mock_version.unpack.return_value = 5
        mock_proxy.get_cached_property.return_value = mock_version

        launcher = PortalLauncher()

        self.assertTrue(launcher.portal_available)
        self.assertEqual(launcher.portal_version, 5)
        self.assertIsNotNone(launcher.bus)

    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.Gio.bus_get_sync')
    def test_portal_launcher_initialization_failure(self, mock_bus_get):
        """Test portal initialization failure."""
        from cloud.ivanbotty.Launcher.helper.portal_launcher import PortalLauncher

        # Make bus_get_sync raise an exception
        mock_bus_get.side_effect = Exception("D-Bus not available")

        launcher = PortalLauncher()

        self.assertFalse(launcher.portal_available)
        self.assertIsNone(launcher.portal_version)
        self.assertIsNone(launcher.bus)

    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.os.path.exists')
    def test_is_flatpak_detection(self, mock_exists):
        """Test Flatpak environment detection."""
        from cloud.ivanbotty.Launcher.helper.portal_launcher import PortalLauncher

        # Test Flatpak environment
        mock_exists.return_value = True
        self.assertTrue(PortalLauncher._is_flatpak())

        # Test non-Flatpak environment
        mock_exists.return_value = False
        self.assertFalse(PortalLauncher._is_flatpak())

    def test_validate_desktop_file_id(self):
        """Test desktop file ID validation."""
        from cloud.ivanbotty.Launcher.helper.portal_launcher import PortalLauncher

        # Valid IDs
        self.assertEqual(PortalLauncher._validate_desktop_file_id("firefox.desktop"), "firefox.desktop")
        self.assertEqual(PortalLauncher._validate_desktop_file_id("  test.desktop  "), "test.desktop")

        # Invalid IDs
        with self.assertRaises(ValueError):
            PortalLauncher._validate_desktop_file_id("")
        
        with self.assertRaises(ValueError):
            PortalLauncher._validate_desktop_file_id("test\nmalicious.desktop")

    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.shutil.which')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.PortalLauncher._is_flatpak')
    def test_get_system_commands_native(self, mock_is_flatpak, mock_which):
        """Test system command generation in native environment."""
        from cloud.ivanbotty.Launcher.helper.portal_launcher import PortalLauncher

        mock_is_flatpak.return_value = False
        # Simulate gtk-launch and xdg-open available
        mock_which.side_effect = lambda cmd: cmd in ["gtk-launch", "xdg-open"]

        launcher = PortalLauncher()
        commands = launcher._get_system_commands("test.desktop")

        # Should include gtk-launch and xdg-open (both available)
        self.assertTrue(any("gtk-launch" in cmd for cmd in commands))
        self.assertTrue(any("xdg-open" in cmd for cmd in commands))
        # kde-open5 not available, check it's not in the list
        has_kde = any("kde-open5" == cmd[0] for cmd in commands)
        self.assertFalse(has_kde)

    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.shutil.which')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.PortalLauncher._is_flatpak')
    def test_get_system_commands_flatpak(self, mock_is_flatpak, mock_which):
        """Test system command generation in Flatpak environment."""
        from cloud.ivanbotty.Launcher.helper.portal_launcher import PortalLauncher

        mock_is_flatpak.return_value = True
        mock_which.return_value = "/usr/bin/flatpak-spawn"

        launcher = PortalLauncher()
        commands = launcher._get_system_commands("test.desktop")

        # All commands should use flatpak-spawn
        for cmd in commands:
            self.assertEqual(cmd[0], "flatpak-spawn")
            self.assertEqual(cmd[1], "--host")

    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.Gio.bus_get_sync')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.Gio.DBusProxy.new_sync')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.subprocess.Popen')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.shutil.which')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.PortalLauncher._is_flatpak')
    def test_open_desktop_app_portal_success(self, mock_is_flatpak, mock_which, 
                                              mock_popen, mock_proxy_new, mock_bus_get):
        """Test successful app launch via portal."""
        from cloud.ivanbotty.Launcher.helper.portal_launcher import PortalLauncher

        mock_is_flatpak.return_value = False
        mock_which.return_value = "/usr/bin/gtk-launch"
        
        # Mock portal components
        mock_bus = MagicMock()
        mock_proxy = MagicMock()
        mock_bus_get.return_value = mock_bus
        
        def proxy_factory(*args, **kwargs):
            proxy = MagicMock()
            # Mock successful portal call
            proxy.call_sync.return_value = None
            return proxy
        
        mock_proxy_new.side_effect = proxy_factory
        mock_version = MagicMock()
        mock_version.unpack.return_value = 5
        mock_proxy.get_cached_property.return_value = mock_version

        launcher = PortalLauncher()
        
        # This should succeed via portal without calling system commands
        launcher.open_desktop_app("firefox.desktop")
        
        # Popen should not be called if portal succeeds
        mock_popen.assert_not_called()

    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.Gio.bus_get_sync')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.subprocess.Popen')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.shutil.which')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.PortalLauncher._is_flatpak')
    def test_open_desktop_app_system_fallback(self, mock_is_flatpak, mock_which, 
                                               mock_popen, mock_bus_get):
        """Test app launch fallback to system commands when portal fails."""
        from cloud.ivanbotty.Launcher.helper.portal_launcher import PortalLauncher
        import subprocess

        # Portal not available
        mock_bus_get.side_effect = Exception("D-Bus not available")
        mock_is_flatpak.return_value = False
        mock_which.return_value = "/usr/bin/gtk-launch"
        
        # Mock successful process - still running after timeout
        mock_process = MagicMock()
        mock_process.wait.side_effect = subprocess.TimeoutExpired("cmd", 0.5)
        mock_process.stderr = None
        mock_popen.return_value = mock_process

        launcher = PortalLauncher()
        launcher.open_desktop_app("firefox.desktop")
        
        # Should have tried system command
        mock_popen.assert_called()

    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.Gio.bus_get_sync')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.shutil.which')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.PortalLauncher._is_flatpak')
    def test_open_desktop_app_all_methods_fail(self, mock_is_flatpak, mock_which, mock_bus_get):
        """Test that RuntimeError is raised when all launch methods fail."""
        from cloud.ivanbotty.Launcher.helper.portal_launcher import PortalLauncher

        # Portal not available
        mock_bus_get.side_effect = Exception("D-Bus not available")
        mock_is_flatpak.return_value = False
        # No system commands available
        mock_which.return_value = None

        launcher = PortalLauncher()
        
        with self.assertRaises(RuntimeError) as context:
            launcher.open_desktop_app("firefox.desktop")
        
        self.assertIn("all methods failed", str(context.exception))

    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.Gio.bus_get_sync')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.Gio.DBusProxy.new_sync')
    def test_get_portal_info(self, mock_proxy_new, mock_bus_get):
        """Test portal info reporting."""
        from cloud.ivanbotty.Launcher.helper.portal_launcher import PortalLauncher

        # Mock portal components
        mock_bus = MagicMock()
        mock_proxy = MagicMock()
        mock_bus_get.return_value = mock_bus
        mock_proxy_new.return_value = mock_proxy
        
        mock_version = MagicMock()
        mock_version.unpack.return_value = 5
        mock_proxy.get_cached_property.return_value = mock_version

        launcher = PortalLauncher()
        info = launcher.get_portal_info()

        self.assertIn("available", info)
        self.assertIn("version", info)
        self.assertIn("available_interfaces", info)
        self.assertIn("is_flatpak", info)
        self.assertTrue(info["available"])

    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.Gio.bus_get_sync')
    @patch('cloud.ivanbotty.Launcher.helper.portal_launcher.Gio.DBusProxy.new_sync')
    def test_interface_detection(self, mock_proxy_new, mock_bus_get):
        """Test that available interfaces are detected correctly."""
        from cloud.ivanbotty.Launcher.helper.portal_launcher import (
            PortalLauncher, 
            LAUNCHER_INTERFACE, 
            OPENURI_INTERFACE
        )

        # Mock portal components
        mock_bus = MagicMock()
        mock_bus_get.return_value = mock_bus
        
        def proxy_factory(*args, **kwargs):
            # Only create OpenURI proxy successfully
            interface = args[6] if len(args) > 6 else kwargs.get('interface_name')
            if interface == OPENURI_INTERFACE or not interface or 'Desktop' in str(interface):
                proxy = MagicMock()
                mock_version = MagicMock()
                mock_version.unpack.return_value = 5
                proxy.get_cached_property.return_value = mock_version
                return proxy
            else:
                raise Exception(f"Interface {interface} not available")
        
        mock_proxy_new.side_effect = proxy_factory

        launcher = PortalLauncher()
        
        # OpenURI should be detected
        self.assertIn(OPENURI_INTERFACE, launcher._available_interfaces)


if __name__ == "__main__":
    unittest.main()
