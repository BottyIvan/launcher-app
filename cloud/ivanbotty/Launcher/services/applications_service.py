import os, gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gio

from cloud.ivanbotty.Launcher.config.config import ALL_APP_DIRS, ICON_DIRS
from cloud.ivanbotty.Launcher.helper.parser import Parser
from cloud.ivanbotty.Launcher.models.applications_model import ApplicationModel

class ApplicationsService:
    """Service for loading and filtering application entries."""

    def __init__(self):
        """Initialize the ApplicationsService with a parser and an empty store."""
        self.parser = Parser()
        self.store = Gio.ListStore(item_type=ApplicationModel)

    def load_applications(self):
        """
        Load application entries from directories specified in ALL_APP_DIRS.

        Parses '.desktop' files into ApplicationModel instances and appends them to the store.
        Ensures each application is loaded only once by name.

        Returns:
            Gio.ListStore: Store containing loaded ApplicationModel instances.
        """
        loaded_names = set()
        self.store.remove_all()
        for app_dir in ALL_APP_DIRS:
            if app_dir.exists() and app_dir.is_dir():
                for file in os.listdir(app_dir):
                    if file.endswith(".desktop"):
                        file_path = os.path.join(app_dir, file)
                        entry_data = self.parser.parse_desktop_entry(file_path)
                        if entry_data and entry_data['name'] not in loaded_names:
                            print(f"Loaded application: {entry_data['name']}")
                            self.store.append(ApplicationModel(
                                type="math",
                                name=entry_data['name'],
                                description=None,
                                exec_cmd=entry_data['exec_cmd'],
                                icon=self.find_icon(entry_data['icon']) if entry_data['icon'] else None
                            ))
                            loaded_names.add(entry_data['name'])
        return self.store
    
    def find_icon(self, icon_name):
        """
        Search for an icon file by name in ICON_DIRS recursively.

        Args:
            icon_name (str): Name of the icon to search for (without extension).

        Returns:
            str or None: Full path to the icon file if found, otherwise None.
        """
        possible_extensions = [".png", ".svg", ".xpm"]

        print(f"Searching for icon: {icon_name}")
        for icon_dir in ICON_DIRS:
            if icon_dir.exists() and icon_dir.is_dir():
                found_icon = self._search_icon_in_dir(icon_dir, icon_name, possible_extensions)
                if found_icon:
                    return found_icon
        return None

    def _search_icon_in_dir(self, icon_dir, icon_name, extensions):
        """
        Helper to search for the icon in a single directory with given extensions.
        """
        for ext in extensions:
            pattern = f"**/{icon_name}{ext}"
            for path in icon_dir.rglob(pattern):
                if path.is_file():
                    return str(path)
        return None

    def filter_applications(self, search_text=""):
        """
        Filter applications by name using the provided search text.

        Args:
            search_text (str): Text to search for in application names.

        Returns:
            Gio.ListStore: Store containing filtered ApplicationModel instances.
        """
        filtered_apps = []
        search_text = search_text.lower()
        # Iterate over all applications in the store
        for i in range(self.store.get_n_items()):
            app = self.store.get_item(i)
            # Check if the application's name contains the search text (case-insensitive)
            if search_text in app.name.lower():
                filtered_apps.append(app)
        # Sort the filtered applications alphabetically by name
        filtered_apps.sort(key=lambda a: a.name.lower())
        # Create a new ListStore for the filtered applications
        filtered_store = Gio.ListStore(item_type=ApplicationModel)
        for app in filtered_apps:
            filtered_store.append(app)
        return filtered_store
