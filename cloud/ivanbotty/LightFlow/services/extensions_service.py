import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gio
from cloud.ivanbotty.LightFlow.models.extension_model import ExtensionModel


class ExtensionService:
    def __init__(self):
        # Initialize a Gio.ListStore to hold ExtensionModel instances
        self.extensions = Gio.ListStore(item_type=ExtensionModel)

    def register(self, extension: ExtensionModel):
        """Add a new extension to the store."""
        self.extensions.append(extension)

    def load_from_config(self, config):
        """
        Load extensions from a configuration dictionary.

        The config should contain an "extensions" key with a list of extension definitions.
        Each extension is registered as an ExtensionModel instance.
        """
        for ext in config.get("extensions", []):
            self.register(
                ExtensionModel(
                    name=ext["name"],
                    description=ext.get("description", ""),
                    enabled=ext.get("enabled", True),
                    service=ext.get("service"),
                    handler=ext.get("handler"),
                    version=ext.get("version"),
                    author=ext.get("author"),
                )
            )

    def list_extensions(self):
        """
        Return the Gio.ListStore containing all registered extensions.
        """
        return self.extensions

    def get_service(self, name):
        """
        Retrieve the service associated with an enabled extension by name.

        Returns:
            The service object if found and enabled, otherwise None.
        """
        for ext in self.extensions:
            if ext.name == name and ext.enabled:
                return ext.service
        return None
