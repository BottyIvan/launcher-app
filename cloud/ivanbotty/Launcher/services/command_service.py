"""Command service for quick system commands.

This module provides a service for managing and executing quick system commands
like opening terminals, file managers, etc.
"""

import gi

from cloud.ivanbotty.Launcher.models.applications_model import ApplicationModel

gi.require_version("Gtk", "4.0")

from gi.repository import Gio


class CommandService:
    """Quick command management service.

    Attributes:
        store: ListStore containing available commands
    """

    def __init__(self) -> None:
        """Initialize the CommandService and register default commands."""
        # We use a ListStore so the controller can bind directly to Gtk.ListBox
        self.store = Gio.ListStore(item_type=ApplicationModel)

        # Register default commands
        self.register_default_commands()

    def register_default_commands(self) -> None:
        """Add basic system commands to the store."""
        self.add_command(ApplicationModel("Terminal", "gnome-terminal", "Open the terminal"))
        self.add_command(ApplicationModel("File Manager", "nautilus", "Open the file manager"))
        self.add_command(
            ApplicationModel("Browser", "xdg-open https://www.google.com", "Open the browser")
        )
        self.add_command(ApplicationModel("Shutdown", "systemctl poweroff", "Shut down the system"))

    def add_command(self, command: ApplicationModel) -> None:
        """Add a new command to the store.

        Args:
            command: ApplicationModel representing the command
        """
        self.store.append(command)

    def filter_commands(self, search_text: str) -> Gio.ListStore:
        """Filter commands by name or description.

        Args:
            search_text: Text to search for in command names and descriptions

        Returns:
            ListStore containing matching commands
        """
        search_text = search_text.lower()
        filtered = Gio.ListStore(item_type=ApplicationModel)
        for i in range(self.store.get_n_items()):
            cmd = self.store.get_item(i)
            if search_text in cmd.name.lower() or search_text in cmd.description.lower():
                filtered.append(cmd)
        return filtered

    def get_command(self, search_text: str) -> ApplicationModel:
        """Return the first command that matches the search text.

        Args:
            search_text: Text to search for

        Returns:
            First matching ApplicationModel or None if no match found
        """
        matches = self.filter_commands(search_text)
        if matches.get_n_items() > 0:
            return matches.get_item(0)
        return None
