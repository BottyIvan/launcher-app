import gi
gi.require_version("Gtk", "4.0")
from gi.repository import GObject
import cloud.ivanbotty.database.sqlite3 as db

class ExtensionModel(GObject.GObject):
    """
    Represents an extension for the Launcher application.

    Attributes:
        name (str): Extension name.
        description (str): Extension description.
        enabled (bool): Whether the extension is enabled.
        cant_disable (bool): Whether the extension can be disabled.
        version (str): Extension version.
        author (str): Extension author.
        service: Associated service identifier.
        handler: Associated handler.
    """

    name = GObject.Property(type=str)
    description = GObject.Property(type=str, default=None)
    enabled = GObject.Property(type=bool, default=True)
    cant_disable = GObject.Property(type=bool, default=False)
    version = GObject.Property(type=str, default=None)
    author = GObject.Property(type=str, default=None)

    def __init__(self, name, description=None, enabled=True, cant_disable=False, service=None, handler=None, version=None, author=None):
        """
        Initialize ExtensionModel.

        Args:
            name (str): Extension name.
            description (str, optional): Extension description.
            enabled (bool, optional): Initial enabled state.
            cant_disable (bool, optional): If True, the extension cannot be disabled.
            service (optional): Service identifier.
            handler (optional): Extension handler.
            version (str, optional): Extension version.
            author (str, optional): Extension author.
        """
        super().__init__()
        self.name = name
        self.description = description
        self.service = service
        self.handler = handler

        # Set enabled state from database if available, otherwise use default and save it
        db_enabled = db.get_extension(service)
        if db_enabled is not None:
            self.enabled = db_enabled
        else:
            self.enabled = enabled
            db.set_extension_enabled(service, enabled)
        self.cant_disable = cant_disable
        self.version = version
        self.author = author
