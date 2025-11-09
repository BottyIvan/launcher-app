"""D-Bus client for communicating with the Launcher daemon.

This module provides a client interface for the Launcher UI to query
cache status, indexing progress, and receive updates from the daemon.
"""

import logging
from typing import Optional, Tuple, Callable

try:
    from gi.repository import GLib, Gio
    DBUS_AVAILABLE = True
except ImportError:
    DBUS_AVAILABLE = False
    GLib = None
    Gio = None

logger = logging.getLogger(__name__)


class LauncherDaemonClient:
    """Client for communicating with the Launcher daemon via D-Bus.

    Provides methods to query cache status, indexing progress, and
    subscribe to daemon signals.
    """

    BUS_NAME = "cloud.ivanbotty.Launcherd"
    OBJECT_PATH = "/cloud/ivanbotty/Launcherd"
    INTERFACE_NAME = "cloud.ivanbotty.Launcherd"

    def __init__(self):
        """Initialize the D-Bus client."""
        if not DBUS_AVAILABLE:
            raise ImportError("D-Bus support requires PyGObject with GLib/Gio")

        self.proxy: Optional[Gio.DBusProxy] = None
        self.connection: Optional[Gio.DBusConnection] = None
        self._signal_subscriptions = []

    def connect(self, timeout_ms: int = 1000) -> bool:
        """Connect to the daemon D-Bus service synchronously.
        
        Note: This method blocks and should not be used during UI startup.
        Use connect_async() instead for non-blocking connection.

        Args:
            timeout_ms: Connection timeout in milliseconds

        Returns:
            True if connected successfully, False otherwise
        """
        try:
            self.connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)

            self.proxy = Gio.DBusProxy.new_sync(
                self.connection,
                Gio.DBusProxyFlags.NONE,
                None,
                self.BUS_NAME,
                self.OBJECT_PATH,
                self.INTERFACE_NAME,
                None
            )

            # Test connection by checking if the service is available
            # This will raise an error if the service is not running
            self.proxy.get_cached_property("Version")

            logger.info("Connected to Launcher daemon")
            return True

        except Exception as e:
            logger.debug(f"Could not connect to daemon: {e}")
            self.proxy = None
            self.connection = None
            return False
    
    def connect_async(self, callback: Callable[[bool], None]) -> None:
        """Connect to the daemon D-Bus service asynchronously.
        
        This method doesn't block and is suitable for use during UI startup.
        The connection happens in the background, and the callback is invoked
        when the connection attempt completes.
        
        Args:
            callback: Function to call with the connection result (True/False)
        """
        def do_connect():
            """Thread function to attempt connection."""
            try:
                self.connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)
                
                # Try to create proxy with DO_NOT_AUTO_START flag first
                # to check if daemon is already running
                try:
                    test_proxy = Gio.DBusProxy.new_sync(
                        self.connection,
                        Gio.DBusProxyFlags.DO_NOT_AUTO_START,
                        None,
                        self.BUS_NAME,
                        self.OBJECT_PATH,
                        self.INTERFACE_NAME,
                        None
                    )
                    # Daemon is already running, use it
                    self.proxy = test_proxy
                    logger.debug("Daemon already running")
                except Exception:
                    # Daemon not running, don't wait for auto-start
                    # Just log and return False
                    logger.debug("Daemon not running and won't auto-start for async connect")
                    GLib.idle_add(lambda: callback(False) or False)
                    return
                
                # Test that we can actually communicate
                self.proxy.get_cached_property("Version")
                
                logger.debug("Async connection to daemon successful")
                GLib.idle_add(lambda: callback(True) or False)
                
            except Exception as e:
                logger.debug(f"Async connection to daemon failed: {e}")
                self.proxy = None
                self.connection = None
                GLib.idle_add(lambda: callback(False) or False)
        
        # Run connection attempt in a background thread
        import threading
        thread = threading.Thread(target=do_connect, daemon=True)
        thread.start()

    def disconnect(self) -> None:
        """Disconnect from the daemon."""
        # Unsubscribe from all signals
        for subscription_id in self._signal_subscriptions:
            if self.connection:
                self.connection.signal_unsubscribe(subscription_id)
        self._signal_subscriptions.clear()

        self.proxy = None
        self.connection = None
        logger.debug("Disconnected from daemon")

    def is_connected(self) -> bool:
        """Check if connected to the daemon.

        Returns:
            True if connected, False otherwise
        """
        return self.proxy is not None

    def get_cache_status(self) -> Optional[Tuple[bool, str, int]]:
        """Get the current cache status from the daemon.

        Returns:
            Tuple of (available, cache_path, last_updated) or None if unavailable
        """
        if not self.proxy:
            logger.debug("Not connected to daemon")
            return None

        try:
            result = self.proxy.call_sync(
                "GetCacheStatus",
                None,
                Gio.DBusCallFlags.NONE,
                30000,  # 30 second timeout (daemon may need time to start via D-Bus activation)
                None
            )

            # Unpack the result: (bool, string, int64)
            available, cache_path, last_updated = result.unpack()
            return (available, cache_path, last_updated)

        except Exception as e:
            logger.debug(f"Error getting cache status: {e}")
            return None

    def get_indexing_status(self) -> Optional[Tuple[bool, float, int]]:
        """Get the current indexing status from the daemon.

        Returns:
            Tuple of (is_indexing, progress, apps_count) or None if unavailable
        """
        if not self.proxy:
            logger.debug("Not connected to daemon")
            return None

        try:
            result = self.proxy.call_sync(
                "GetIndexingStatus",
                None,
                Gio.DBusCallFlags.NONE,
                30000,  # 30 second timeout (daemon may need time to start via D-Bus activation)
                None
            )

            # Unpack the result: (bool, double, int32)
            is_indexing, progress, apps_count = result.unpack()
            return (is_indexing, progress, apps_count)

        except Exception as e:
            logger.debug(f"Error getting indexing status: {e}")
            return None

    def force_update(self) -> bool:
        """Request the daemon to force an immediate cache update.

        Returns:
            True if request was sent successfully, False otherwise
        """
        if not self.proxy:
            logger.debug("Not connected to daemon")
            return False

        try:
            self.proxy.call_sync(
                "ForceUpdate",
                None,
                Gio.DBusCallFlags.NONE,
                30000,  # 30 second timeout (daemon may need time to start via D-Bus activation)
                None
            )
            logger.info("Force update requested")
            return True

        except Exception as e:
            logger.error(f"Error requesting force update: {e}")
            return False

    def subscribe_to_cache_updated(self, callback: Callable[[int, int], None]) -> bool:
        """Subscribe to CacheUpdated signals from the daemon.

        Args:
            callback: Function to call when cache is updated.
                     Receives (apps_count, timestamp) as arguments.

        Returns:
            True if subscribed successfully, False otherwise
        """
        if not self.connection:
            logger.debug("Not connected to daemon")
            return False

        try:
            def signal_handler(
                connection: Gio.DBusConnection,
                sender_name: str,
                object_path: str,
                interface_name: str,
                signal_name: str,
                parameters: GLib.Variant
            ):
                if signal_name == "CacheUpdated":
                    apps_count, timestamp = parameters.unpack()
                    try:
                        callback(apps_count, timestamp)
                    except Exception as e:
                        logger.error(f"Error in CacheUpdated callback: {e}")

            subscription_id = self.connection.signal_subscribe(
                self.BUS_NAME,
                self.INTERFACE_NAME,
                "CacheUpdated",
                self.OBJECT_PATH,
                None,  # arg0
                Gio.DBusSignalFlags.NONE,
                signal_handler
            )

            self._signal_subscriptions.append(subscription_id)
            logger.debug("Subscribed to CacheUpdated signal")
            return True

        except Exception as e:
            logger.error(f"Error subscribing to CacheUpdated: {e}")
            return False

    def subscribe_to_indexing_progress(self, callback: Callable[[float, int], None]) -> bool:
        """Subscribe to IndexingProgress signals from the daemon.

        Args:
            callback: Function to call when indexing progress updates.
                     Receives (progress, apps_count) as arguments.

        Returns:
            True if subscribed successfully, False otherwise
        """
        if not self.connection:
            logger.debug("Not connected to daemon")
            return False

        try:
            def signal_handler(
                connection: Gio.DBusConnection,
                sender_name: str,
                object_path: str,
                interface_name: str,
                signal_name: str,
                parameters: GLib.Variant
            ):
                if signal_name == "IndexingProgress":
                    progress, apps_count = parameters.unpack()
                    try:
                        callback(progress, apps_count)
                    except Exception as e:
                        logger.error(f"Error in IndexingProgress callback: {e}")

            subscription_id = self.connection.signal_subscribe(
                self.BUS_NAME,
                self.INTERFACE_NAME,
                "IndexingProgress",
                self.OBJECT_PATH,
                None,  # arg0
                Gio.DBusSignalFlags.NONE,
                signal_handler
            )

            self._signal_subscriptions.append(subscription_id)
            logger.debug("Subscribed to IndexingProgress signal")
            return True

        except Exception as e:
            logger.error(f"Error subscribing to IndexingProgress: {e}")
            return False

    def is_daemon_available(self) -> bool:
        """Check if the daemon is available without maintaining a connection.

        Returns:
            True if daemon is running, False otherwise
        """
        try:
            connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)

            # Use DO_NOT_AUTO_START to avoid starting the daemon
            proxy = Gio.DBusProxy.new_sync(
                connection,
                Gio.DBusProxyFlags.DO_NOT_AUTO_START,
                None,
                self.BUS_NAME,
                self.OBJECT_PATH,
                self.INTERFACE_NAME,
                None
            )

            # Try to get a property to verify the service is responsive
            version = proxy.get_cached_property("Version")
            return version is not None

        except Exception as e:
            logger.debug(f"Daemon not available: {e}")
            return False
