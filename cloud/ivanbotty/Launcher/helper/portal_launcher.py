import logging
import subprocess
import shutil
import os
from typing import Optional, Dict, Any, List, Set
from contextlib import contextmanager
from gi.repository import Gio, GLib

logger = logging.getLogger(__name__)

PORTAL_BUS = "org.freedesktop.portal.Desktop"
PORTAL_PATH = "/org/freedesktop/portal/desktop"
LAUNCHER_INTERFACE = "org.freedesktop.portal.Launcher"
OPENURI_INTERFACE = "org.freedesktop.portal.OpenURI"
DESKTOP_INTERFACE = "org.freedesktop.portal.Desktop"


class PortalLauncher:
    """Desktop app launcher using xdg-desktop-portal with system fallback."""

    def __init__(self):
        self.bus: Optional[Gio.DBusConnection] = None
        self.proxy: Optional[Gio.DBusProxy] = None
        self.portal_available = False
        self.portal_version: Optional[int] = None
        self._proxy_cache: Dict[str, Gio.DBusProxy] = {}
        self._available_interfaces: Set[str] = set()
        self._initialize_portal()

    def __del__(self):
        self._cleanup()

    def _initialize_portal(self) -> None:
        """Setup portal connection and detect available interfaces."""
        try:
            self.bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
            self.proxy = Gio.DBusProxy.new_sync(
                self.bus,
                Gio.DBusProxyFlags.NONE,
                None,
                PORTAL_BUS,
                PORTAL_PATH,
                DESKTOP_INTERFACE,
                None,
            )
            self.portal_available = True
            self.portal_version = self._get_portal_version()
            self._detect_available_interfaces()
            logger.info(f"Portal initialized (v{self.portal_version}, interfaces: {self._available_interfaces})")
        except Exception as e:
            logger.warning(f"Portal initialization failed: {e}")
            self._reset_portal_state()

    def _reset_portal_state(self) -> None:
        """Reset portal state."""
        self._cleanup()
        self.portal_available = False
        self.portal_version = None
        self._available_interfaces.clear()

    def _cleanup(self) -> None:
        """Release resources."""
        self._proxy_cache.clear()
        self.bus = None
        self.proxy = None

    def _get_portal_version(self) -> Optional[int]:
        """Return portal version."""
        if not self.proxy:
            return None
        try:
            result = self.proxy.get_cached_property("version")
            return result.unpack() if result is not None else None
        except Exception as e:
            logger.debug(f"Version check failed: {e}")
            return None

    def _detect_available_interfaces(self) -> None:
        """Detect which portal interfaces are available."""
        # Try to create proxies for each interface to see if they're available
        for interface in [LAUNCHER_INTERFACE, OPENURI_INTERFACE]:
            try:
                proxy = self._get_portal_proxy(interface)
                if proxy:
                    self._available_interfaces.add(interface)
                    logger.debug(f"Detected available interface: {interface}")
            except Exception as e:
                logger.debug(f"Interface {interface} not available: {e}")

    def _get_portal_proxy(self, interface: str) -> Optional[Gio.DBusProxy]:
        """Return cached D-Bus proxy for interface."""
        if not self.bus:
            return None
        if interface not in self._proxy_cache:
            try:
                self._proxy_cache[interface] = Gio.DBusProxy.new_sync(
                    self.bus,
                    Gio.DBusProxyFlags.NONE,
                    None,
                    PORTAL_BUS,
                    PORTAL_PATH,
                    interface,
                    None,
                )
            except Exception as e:
                logger.debug(f"Proxy failed for {interface}: {e}")
                return None
        return self._proxy_cache.get(interface)

    def _call_portal_method(self, interface: str, method: str, args: GLib.Variant, timeout: int = 30000) -> bool:
        """Invoke portal method with better error handling."""
        # Check if interface is available
        if interface not in self._available_interfaces:
            logger.debug(f"Interface {interface} not in available interfaces")
            return False
            
        proxy = self._get_portal_proxy(interface)
        if not proxy:
            logger.debug(f"Failed to get proxy for {interface}")
            return False
            
        try:
            logger.info(f"Attempting to call {interface}.{method}")
            result = proxy.call_sync(method, args, Gio.DBusCallFlags.NONE, timeout, None)
            logger.info(f"Successfully launched via {interface}.{method}")
            return True
        except GLib.GError as e:
            if 'UnknownMethod' in str(e):
                logger.debug(f"{interface}.{method} not available: UnknownMethod")
                # Remove from available interfaces so we don't try again
                self._available_interfaces.discard(interface)
            elif 'NotFound' in str(e):
                logger.debug(f"{interface}.{method} failed: Application not found")
            else:
                logger.debug(f"{interface}.{method} error: {e}")
            return False
        except Exception as e:
            logger.warning(f"{interface}.{method} unexpected error: {e}")
            return False

    @staticmethod
    def _is_flatpak() -> bool:
        """Detect Flatpak environment."""
        return os.path.exists("/.flatpak-info")

    def _get_system_commands(self, desktop_file_id: str) -> List[List[str]]:
        """Return system launcher commands in order of preference."""
        base_commands = [
            ["gtk-launch", desktop_file_id],
            ["xdg-open", f"application://{desktop_file_id}"],
            ["kde-open5", f"application://{desktop_file_id}"],
        ]
        
        if self._is_flatpak():
            # Inside Flatpak, use flatpak-spawn to run commands on host
            if not shutil.which("flatpak-spawn"):
                logger.warning("Running in Flatpak but flatpak-spawn not found")
                return []
            return [["flatpak-spawn", "--host"] + cmd for cmd in base_commands]
        else:
            # Filter to only include commands that exist
            available_commands = []
            for cmd in base_commands:
                if shutil.which(cmd[0]):
                    available_commands.append(cmd)
            return available_commands

    def _try_system_launchers(self, desktop_file_id: str) -> bool:
        """Try system launcher commands as fallback."""
        commands = self._get_system_commands(desktop_file_id)
        
        if not commands:
            logger.warning("No system launcher commands available")
            return False
        
        for cmd in commands:
            # Extract command name for logging
            # In Flatpak: ["flatpak-spawn", "--host", "actual-command", ...]
            # Native: ["actual-command", ...]
            if self._is_flatpak() and len(cmd) > 2:
                cmd_name = cmd[2]  # The actual command after flatpak-spawn --host
            elif len(cmd) > 0:
                cmd_name = cmd[0]  # The command itself
            else:
                logger.warning("Malformed command in list, skipping")
                continue
            
            try:
                logger.info(f"Attempting to launch via system command: {' '.join(cmd)}")
                # Use Popen to launch in background without waiting
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Give it a moment to fail if it's going to fail immediately
                try:
                    return_code = process.wait(timeout=0.5)
                    if return_code != 0:
                        stderr = process.stderr.read() if process.stderr else ""
                        logger.debug(f"Command {cmd_name} failed with code {return_code}: {stderr}")
                        continue
                except subprocess.TimeoutExpired:
                    # Process is still running, assume success
                    pass
                
                logger.info(f"Successfully launched via system command: {cmd_name}")
                return True
                
            except FileNotFoundError:
                logger.debug(f"Command not found: {cmd_name}")
            except PermissionError as e:
                logger.debug(f"Permission denied for {cmd_name}: {e}")
            except subprocess.SubprocessError as e:
                logger.debug(f"Command {cmd_name} failed: {e}")
            except Exception as e:
                logger.warning(f"Unexpected error with {cmd_name}: {e}")
        
        logger.warning("All system launcher commands failed")
        return False

    @staticmethod
    def _validate_desktop_file_id(desktop_file_id: str) -> str:
        """Validate desktop file ID."""
        if not desktop_file_id or not desktop_file_id.strip():
            raise ValueError("desktop_file_id empty")
        desktop_file_id = desktop_file_id.strip()
        if any(char in desktop_file_id for char in ['\n', '\r', '\0']):
            raise ValueError("desktop_file_id invalid chars")
        return desktop_file_id

    def open_desktop_app(self, desktop_file_id: str, options: Optional[Dict[str, Any]] = None) -> None:
        """Launch desktop application using best available method.
        
        Tries methods in this order:
        1. org.freedesktop.portal.Launcher.LaunchApplication (if available)
        2. org.freedesktop.portal.OpenURI.OpenURI (if available)
        3. System commands: gtk-launch, xdg-open, kde-open5
        
        Args:
            desktop_file_id: The desktop file ID (e.g., 'firefox.desktop')
            options: Optional dictionary of portal options
            
        Raises:
            RuntimeError: If all launch methods fail
        """
        desktop_file_id = self._validate_desktop_file_id(desktop_file_id)
        logger.info(f"Attempting to launch application: {desktop_file_id}")
        
        # Prepare portal arguments
        portal_options = options or {}
        # Parent window handle (empty string means no parent)
        parent_window = ""
        uri = f"application://{desktop_file_id}"
        
        # Try portal methods if available
        if self.portal_available and self.bus:
            logger.debug("Portal is available, trying portal methods")
            
            # Method 1: Try Launcher interface (preferred, but newer)
            if LAUNCHER_INTERFACE in self._available_interfaces:
                logger.debug("Trying Launcher.LaunchApplication")
                # LaunchApplication expects (parent_window, desktop_file_id, options)
                args = GLib.Variant("(ssa{sv})", (parent_window, desktop_file_id, portal_options))
                if self._call_portal_method(LAUNCHER_INTERFACE, "LaunchApplication", args):
                    return
            
            # Method 2: Try OpenURI interface (more common, should work with application:// URIs)
            if OPENURI_INTERFACE in self._available_interfaces:
                logger.debug("Trying OpenURI.OpenURI")
                # OpenURI expects (parent_window, uri, options)
                args = GLib.Variant("(ssa{sv})", (parent_window, uri, portal_options))
                if self._call_portal_method(OPENURI_INTERFACE, "OpenURI", args):
                    return
            
            logger.info("Portal methods failed or unavailable, falling back to system commands")
        else:
            logger.debug("Portal not available, using system commands directly")
        
        # Method 3: System fallback
        if self._try_system_launchers(desktop_file_id):
            return
        
        # All methods failed
        error_msg = f"Failed to launch application '{desktop_file_id}' - all methods failed"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    @contextmanager
    def _ensure_portal(self):
        """Ensure portal availability."""
        if not self.portal_available:
            self._initialize_portal()
        yield

    def is_portal_available(self) -> bool:
        """Return portal availability."""
        return self.portal_available and self.bus is not None

    def get_portal_info(self) -> Dict[str, Any]:
        """Return portal debug info."""
        return {
            "available": self.portal_available,
            "version": self.portal_version,
            "available_interfaces": list(self._available_interfaces),
            "is_flatpak": self._is_flatpak(),
        }
