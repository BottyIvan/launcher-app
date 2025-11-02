import gi
import subprocess
import logging

gi.require_version("Gtk", "4.0")
from gi.repository import GObject

logger = logging.getLogger(__name__)


class ApplicationModel(GObject.GObject):
    """
    Model representing an application with properties for type, name, description,
    execution command, and icon.
    """

    type = GObject.Property(type=str)
    name = GObject.Property(type=str)
    description = GObject.Property(type=str, default=None)
    exec_cmd = GObject.Property(type=str, default=None)
    icon = GObject.Property(type=str, default=None)

    def __init__(self, type, name, description=None, exec_cmd=None, icon=None):
        """
        Initialize the ApplicationModel.

        Args:
            type (str): The type of the application.
            name (str): The name of the application.
            description (str, optional): Description of the application.
            exec_cmd (str, optional): Command to execute the application.
            icon (str, optional): Path to the application's icon.
        """
        super().__init__()
        self.type = type
        self.name = name
        self.description = description
        self.exec_cmd = exec_cmd
        self.icon = icon

    def run(self):
        """
        Run the application's command in the background.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        try:
            subprocess.Popen(self.exec_cmd, shell=True)
            return True
        except Exception as e:
            logger.error(f"Error executing command exec_cmd={self.exec_cmd}: {e}")
            return False
