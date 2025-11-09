import logging
import os

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gio

from cloud.ivanbotty.Launcher.config.config import ALL_APP_DIRS, ICON_DIRS
from cloud.ivanbotty.Launcher.helper.parser import Parser
from cloud.ivanbotty.Launcher.models.applications_model import ApplicationModel

logger = logging.getLogger(__name__)


class ApplicationsService:
    """Service for loading and filtering application entries."""

    def __init__(self):
        """Initialize the ApplicationsService with a parser and an empty store."""
        self.parser = Parser()
        self.store = Gio.ListStore(item_type=ApplicationModel)
        self._icon_cache = {}  # Cache for icon paths
        self._desktop_cache = {}  # Cache for parsed desktop entries

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
            self._load_applications_from_dir(app_dir, loaded_names)
        return self.store
    
    def load_applications_from_cache(self, cache_path: str) -> bool:
        """
        Load applications from a cache file created by the daemon.
        
        Args:
            cache_path: Path to the cache JSON file
            
        Returns:
            True if successfully loaded from cache, False otherwise
        """
        import json
        
        try:
            if not os.path.exists(cache_path):
                logger.debug(f"Cache file not found: {cache_path}")
                return False
            
            # Check if cache is recent (less than 1 hour old)
            cache_age = os.path.getmtime(cache_path)
            import time
            if time.time() - cache_age > 3600:
                logger.debug(f"Cache file too old: {cache_path}")
                return False
            
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            logger.info(f"Loading {len(cache_data)} applications from cache")
            self.store.remove_all()
            
            for entry_data in cache_data:
                try:
                    # Create ApplicationModel from cached data
                    app = ApplicationModel(
                        type=entry_data.get('type', 'Application'),
                        name=entry_data.get('name', ''),
                        description=entry_data.get('description', None),
                        exec_cmd=entry_data.get('exec_cmd', ''),
                        desktop_id=entry_data.get('desktop_id', ''),
                        icon=entry_data.get('icon', None),
                    )
                    self.store.append(app)
                except Exception as e:
                    logger.debug(f"Error loading cached app: {e}")
                    continue
            
            logger.info(f"Successfully loaded {self.store.get_n_items()} applications from cache")
            return True
            
        except Exception as e:
            logger.warning(f"Error loading from cache: {e}")
            return False

    def _load_applications_from_dir(self, app_dir, loaded_names):
        """Helper to load applications from a single directory."""
        if not (app_dir.exists() and app_dir.is_dir()):
            return
        for file in os.listdir(app_dir):
            if not file.endswith(".desktop"):
                continue
            file_path = os.path.join(app_dir, file)
            self._try_load_application(file_path, loaded_names)

    def _try_load_application(self, file_path, loaded_names):
        """Helper to parse and append a single application if not already loaded."""
        # Check cache first
        if file_path in self._desktop_cache:
            entry_data = self._desktop_cache[file_path]
        else:
            entry_data = self.parser.parse_desktop_entry(file_path)
            if entry_data:
                self._desktop_cache[file_path] = entry_data

        if not entry_data:
            return
        app_name = entry_data["name"]
        if app_name in loaded_names:
            return
        logger.debug(f"Loaded application: app_name={app_name}")
        self.store.append(
            ApplicationModel(
                type=entry_data["type"],
                name=app_name,
                description=None,
                exec_cmd=entry_data["exec_cmd"],
                desktop_id=os.path.basename(file_path),
                icon=self.find_icon(entry_data["icon"]) if entry_data["icon"] else None,
            )
        )
        loaded_names.add(app_name)

    def find_icon(self, icon_name):
        """
        Search for an icon file by name in ICON_DIRS recursively.

        Args:
            icon_name (str): Name of the icon to search for (without extension).

        Returns:
            str or None: Full path to the icon file if found, otherwise None.
        """
        # Check cache first
        if icon_name in self._icon_cache:
            return self._icon_cache[icon_name]

        possible_extensions = [".png", ".svg", ".xpm"]

        logger.debug(f"Searching for icon: icon_name={icon_name}")
        for icon_dir in ICON_DIRS:
            if icon_dir.exists() and icon_dir.is_dir():
                found_icon = self._search_icon_in_dir(icon_dir, icon_name, possible_extensions)
                if found_icon:
                    self._icon_cache[icon_name] = found_icon
                    return found_icon

        # Cache negative results too to avoid repeated searches
        self._icon_cache[icon_name] = None
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
        filtered_store = Gio.ListStore(item_type=ApplicationModel)

        search_text_lower = search_text.lower() if search_text else ""

        # Collect matching apps in a list for sorting
        filtered_apps = []
        for i in range(self.store.get_n_items()):
            app = self.store.get_item(i)
            # Check if the application's name contains the search text (case-insensitive)
            if not search_text_lower or search_text_lower in app.name.lower():
                filtered_apps.append(app)

        # Sort once before adding to store
        filtered_apps.sort(key=lambda a: a.name.lower())

        # Add sorted apps to the filtered store
        for app in filtered_apps:
            filtered_store.append(app)

        return filtered_store
