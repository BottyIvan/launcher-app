import logging
from gi.repository import Gio, GLib

logger = logging.getLogger(__name__)

PORTAL_BUS = "org.freedesktop.portal.Desktop"
PORTAL_PATH = "/org/freedesktop/portal/desktop"
PORTAL_INTERFACE = "org.freedesktop.portal.OpenURI"


class PortalLauncher:
    """Wrapper to launch apps via xdg-desktop-portal."""

    def __init__(self):
        self.bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        try:
            self.proxy = Gio.DBusProxy.new_sync(
                self.bus,
                Gio.DBusProxyFlags.NONE,
                None,
                PORTAL_BUS,
                PORTAL_PATH,
                PORTAL_INTERFACE,
                None,
            )
            self.portal_available = True
        except Exception as e:
            logger.warning(f"Portal not available: {e}")
            self.portal_available = False

    def is_available(self):
        """Returns True if the portal is available."""
        return self.portal_available

    def open_desktop_app(self, desktop_file_id: str):
        """
        Uses the portal to launch a registered app (e.g. org.gnome.Nautilus.desktop).
        desktop_file_id should be like 'org.gnome.Nautilus.desktop'
        """
        if not self.portal_available:
            raise RuntimeError("Portal not available")

        try:
            args = GLib.Variant("(ssa{sv})", ("", f"application://{desktop_file_id}", {}))
            logger.debug(f"Portal available: {self.portal_available}")
            logger.debug(f"Bus: {self.bus}")
            logger.debug(f"Proxy: {self.proxy}")
            logger.debug(f"Desktop file ID: {desktop_file_id}")
            logger.debug(f"URI: application://{desktop_file_id}")
            logger.debug(f"args: {args}")
            logger.debug(f"args type: {type(args)}")
            logger.debug("Calling portal OpenURI method...")
            
            result = self.proxy.call_sync(
                "OpenURI",
                args,
                Gio.DBusCallFlags.NONE,
                -1,
                None,
            )
            
            logger.debug(f"Portal call result: {result}")
            logger.debug(f"Portal call result type: {type(result)}")
            logger.info(f"Successfully launched {desktop_file_id} via portal")
        except Exception as e:
            logger.error(f"Portal launch error for {desktop_file_id}: {e}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Portal available at time of error: {self.portal_available}")
            logger.debug(f"Exception details: {str(e)}")
            raise
