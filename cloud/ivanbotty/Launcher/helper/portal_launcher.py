import logging
import subprocess
import shutil
import os
from typing import Optional, Dict, Any, List
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
        self._initialize_portal()

    def __del__(self):
        self._cleanup()

    def _initialize_portal(self) -> None:
        """Setup portal connection."""
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
            logger.debug(f"Portal ready (v{self.portal_version})")
        except Exception as e:
            logger.warning(f"Portal init failed: {e}")
            self._reset_portal_state()

    def _reset_portal_state(self) -> None:
        """Reset portal state."""
        self._cleanup()
        self.portal_available = False
        self.portal_version = None

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
        """Invoke portal method."""
        proxy = self._get_portal_proxy(interface)
        if not proxy:
            return False
        try:
            proxy.call_sync(method, args, Gio.DBusCallFlags.NONE, timeout, None)
            logger.info(f"Launched: {interface}.{method}")
            return True
        except GLib.GError as e:
            logger.debug(f"{interface}.{method} error: {e}")
            return False
        except Exception as e:
            logger.warning(f"{interface}.{method} unexpected: {e}")
            return False

    @staticmethod
    def _is_flatpak() -> bool:
        """Detect Flatpak environment."""
        return os.path.exists("/.flatpak-info")

    def _get_system_commands(self, desktop_file_id: str) -> List[List[str]]:
        """Return system launcher commands."""
        if self._is_flatpak():
            if not shutil.which("flatpak-spawn"):
                return []
            return [
                ["flatpak-spawn", "--host", "gtk-launch", desktop_file_id],
                ["flatpak-spawn", "--host", "xdg-open", f"application://{desktop_file_id}"],
                ["flatpak-spawn", "--host", "kde-open5", f"application://{desktop_file_id}"],
            ]
        else:
            return [
                ["gtk-launch", desktop_file_id],
                ["kde-open5", f"application://{desktop_file_id}"],
                ["xdg-open", f"application://{desktop_file_id}"],
            ]

    def _try_system_launchers(self, desktop_file_id: str) -> bool:
        """Try system launcher commands."""
        commands = self._get_system_commands(desktop_file_id)
        for cmd in commands:
            try:
                subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    text=True
                )
                logger.info(f"Launched: {cmd[0]}")
                return True
            except FileNotFoundError:
                logger.debug(f"Not found: {cmd[0]}")
            except subprocess.SubprocessError as e:
                logger.debug(f"{cmd[0]} failed: {e}")
            except Exception as e:
                logger.debug(f"{cmd[0]} error: {e}")
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
        """Launch desktop application."""
        desktop_file_id = self._validate_desktop_file_id(desktop_file_id)
        portal_options = options or {}
        args = GLib.Variant("(ssa{sv})", ("", f"application://{desktop_file_id}", portal_options))

        # Try portal methods
        if self.portal_available and self.bus:
            if self.portal_version and self.portal_version >= 5:
                if self._call_portal_method(LAUNCHER_INTERFACE, "LaunchApplication", args):
                    return
            if self._call_portal_method(OPENURI_INTERFACE, "OpenURI", args):
                return
            logger.warning("Portal failed, using system launcher")

        # System fallback
        if self._try_system_launchers(desktop_file_id):
            return

        raise RuntimeError(f"Launch failed: {desktop_file_id}")

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
            "cached_proxies": list(self._proxy_cache.keys()),
        }
