import gi
import subprocess
import logging

gi.require_version("Gtk", "4.0")
from gi.repository import GObject

logger = logging.getLogger(__name__)

from cloud.ivanbotty.Launcher.helper.portal_launcher import PortalLauncher


class ApplicationModel(GObject.GObject):
    """
    Model representing an application with properties for type, name, description,
    execution command, desktop ID, and icon.
    """

    type = GObject.Property(type=str)
    name = GObject.Property(type=str)
    description = GObject.Property(type=str, default=None)
    exec_cmd = GObject.Property(type=str, default=None)
    desktop_id = GObject.Property(type=str, default=None)
    icon = GObject.Property(type=str, default=None)

    def __init__(self, type, name, description=None, exec_cmd=None, icon=None, desktop_id=None):
        """
        Initialize the ApplicationModel.

        Args:
            type (str): The type of the application.
            name (str): The name of the application.
            description (str, optional): Description of the application.
            exec_cmd (str, optional): Command to execute the application.
            desktop_id (str, optional): Desktop ID of the application.
            icon (str, optional): Path to the application's icon.
        """
        super().__init__()
        self.portal_launcher = PortalLauncher()
        self.type = type
        self.name = name
        self.description = description
        self.exec_cmd = exec_cmd
        self.desktop_id = desktop_id
        self.icon = icon

    def run(self):
        """
        Run the application's command in the background.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        # Attempt to launch the application using PortalLauncher if available and desktop_id is set.
        # If PortalLauncher is unavailable or fails, fall back to executing the command directly.
        if self.portal_launcher.is_available() and self.desktop_id:
            try:
                self.portal_launcher.open_desktop_app(self.desktop_id)
            except Exception as e:
                logger.error(f"Failed to launch via PortalLauncher (desktop_id={self.desktop_id}): {e}")

        try:
            subprocess.Popen(self.exec_cmd, shell=True)
            return True
        except Exception as e:
            logger.error(f"Error executing command exec_cmd={self.exec_cmd}: {e}")
            return False
