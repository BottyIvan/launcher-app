"""D-Bus service for Launcher daemon.

This module provides a D-Bus service that allows the Launcher UI to communicate
with the background daemon for cache status updates and indexing progress.
"""

import logging
import os
import time
from typing import Optional, Tuple

try:
    from gi.repository import GLib, Gio
    DBUS_AVAILABLE = True
except ImportError:
    DBUS_AVAILABLE = False
    GLib = None
    Gio = None

logger = logging.getLogger(__name__)

# D-Bus interface definition
DBUS_INTERFACE_XML = """
<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN"
 "http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">
<node>
  <interface name="cloud.ivanbotty.Launcherd">
    <method name="GetCacheStatus">
      <arg direction="out" type="b" name="available"/>
      <arg direction="out" type="s" name="cache_path"/>
      <arg direction="out" type="x" name="last_updated"/>
    </method>
    <method name="GetIndexingStatus">
      <arg direction="out" type="b" name="is_indexing"/>
      <arg direction="out" type="d" name="progress"/>
      <arg direction="out" type="i" name="apps_count"/>
    </method>
    <method name="ForceUpdate"/>
    <signal name="CacheUpdated">
      <arg type="i" name="apps_count"/>
      <arg type="x" name="timestamp"/>
    </signal>
    <signal name="IndexingProgress">
      <arg type="d" name="progress"/>
      <arg type="i" name="apps_count"/>
    </signal>
    <property name="Version" type="s" access="read"/>
  </interface>
</node>
"""

class LauncherdDBusService:
    """D-Bus service for the Launcher daemon.

    Provides methods for querying cache status, indexing progress,
    and emitting signals when the cache is updated.
    """

    BUS_NAME = "cloud.ivanbotty.Launcherd"
    OBJECT_PATH = "/cloud/ivanbotty/Launcherd"
    VERSION = "0.0.1"

    def __init__(self, cache_path: str):
        """Initialize the D-Bus service.

        Args:
            cache_path: Path to the applications cache file
        """
        if not DBUS_AVAILABLE:
            raise ImportError("D-Bus support requires PyGObject with GLib/Gio")

        self.cache_path = cache_path
        self.is_indexing = False
        self.progress = 0.0
        self.apps_count = 0
        self.connection: Optional[Gio.DBusConnection] = None
        self.registration_id: Optional[int] = None
        self.name_owner_id: Optional[int] = None

        # Parse the D-Bus interface
        self.node_info = Gio.DBusNodeInfo.new_for_xml(DBUS_INTERFACE_XML)
        self.interface_info = self.node_info.lookup_interface(self.BUS_NAME)

    def start(self) -> bool:
        """Start the D-Bus service.

        Returns:
            True if service started successfully, False otherwise
        """
        try:
            # Get session bus
            self.connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)

            # Register object on the bus
            self.registration_id = self.connection.register_object(
                self.OBJECT_PATH,
                self.interface_info,
                self._handle_method_call,
                self._handle_get_property,
                None  # No settable properties
            )

            # Own the bus name
            self.name_owner_id = Gio.bus_own_name_on_connection(
                self.connection,
                self.BUS_NAME,
                Gio.BusNameOwnerFlags.NONE,
                None,  # name_acquired_callback
                None   # name_lost_callback
            )

            logger.info(f"D-Bus service started: {self.BUS_NAME}")
            return True

        except Exception as e:
            logger.error(f"Failed to start D-Bus service: {e}")
            return False

    def stop(self) -> None:
        """Stop the D-Bus service."""
        if self.registration_id and self.connection:
            self.connection.unregister_object(self.registration_id)
            self.registration_id = None

        if self.name_owner_id:
            Gio.bus_unown_name(self.name_owner_id)
            self.name_owner_id = None

        self.connection = None
        logger.info("D-Bus service stopped")

    def _handle_method_call(
        self,
        connection: Gio.DBusConnection,
        sender: str,
        object_path: str,
        interface_name: str,
        method_name: str,
        parameters: GLib.Variant,
        invocation: Gio.DBusMethodInvocation
    ) -> None:
        """Handle D-Bus method calls."""
        try:
            if method_name == "GetCacheStatus":
                result = self._get_cache_status()
                invocation.return_value(GLib.Variant("(bsx)", result))

            elif method_name == "GetIndexingStatus":
                result = self._get_indexing_status()
                invocation.return_value(GLib.Variant("(bdi)", result))

            elif method_name == "ForceUpdate":
                # Signal that a force update was requested
                # The main loop should handle this
                invocation.return_value(None)

            else:
                invocation.return_dbus_error(
                    "org.freedesktop.DBus.Error.UnknownMethod",
                    f"Method {method_name} not found"
                )

        except Exception as e:
            logger.error(f"Error handling method {method_name}: {e}")
            invocation.return_dbus_error(
                "org.freedesktop.DBus.Error.Failed",
                str(e)
            )

    def _handle_get_property(
        self,
        connection: Gio.DBusConnection,
        sender: str,
        object_path: str,
        interface_name: str,
        property_name: str
    ) -> GLib.Variant:
        """Handle D-Bus property reads."""
        if property_name == "Version":
            return GLib.Variant("s", self.VERSION)
        return None

    def _get_cache_status(self) -> Tuple[bool, str, int]:
        """Get the current cache status.

        Returns:
            Tuple of (available, cache_path, last_updated)
        """
        available = os.path.exists(self.cache_path)
        last_updated = 0

        if available:
            try:
                last_updated = int(os.path.getmtime(self.cache_path))
            except OSError:
                pass

        return (available, self.cache_path, last_updated)

    def _get_indexing_status(self) -> Tuple[bool, float, int]:
        """Get the current indexing status.

        Returns:
            Tuple of (is_indexing, progress, apps_count)
        """
        return (self.is_indexing, self.progress, self.apps_count)

    def update_indexing_progress(self, progress: float, apps_count: int) -> None:
        """Update indexing progress and emit signal.

        Args:
            progress: Progress from 0.0 to 1.0
            apps_count: Number of applications indexed so far
        """
        self.progress = max(0.0, min(1.0, progress))
        self.apps_count = apps_count

        # Emit IndexingProgress signal
        if self.connection:
            try:
                self.connection.emit_signal(
                    None,  # destination (broadcast to all)
                    self.OBJECT_PATH,
                    self.BUS_NAME,
                    "IndexingProgress",
                    GLib.Variant("(di)", (self.progress, self.apps_count))
                )
            except Exception as e:
                logger.debug(f"Error emitting IndexingProgress signal: {e}")

    def emit_cache_updated(self, apps_count: int) -> None:
        """Emit CacheUpdated signal.

        Args:
            apps_count: Number of applications in the updated cache
        """
        timestamp = int(time.time())

        if self.connection:
            try:
                self.connection.emit_signal(
                    None,  # destination (broadcast to all)
                    self.OBJECT_PATH,
                    self.BUS_NAME,
                    "CacheUpdated",
                    GLib.Variant("(ix)", (apps_count, timestamp))
                )
                logger.info(f"Cache updated signal emitted: {apps_count} apps")
            except Exception as e:
                logger.error(f"Error emitting CacheUpdated signal: {e}")

    def set_indexing_state(self, is_indexing: bool) -> None:
        """Set the indexing state.

        Args:
            is_indexing: True if currently indexing, False otherwise
        """
        self.is_indexing = is_indexing
        if not is_indexing:
            self.progress = 1.0
