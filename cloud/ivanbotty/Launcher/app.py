import gi, yaml

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw

from .services.extensions_service import ExtensionService
from .controller.keyboard_controller import KeyboardController
from .controller.search_controller import SearchController
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES
from .widget.window import Window
from .widget.search_entry import SearchEntry
from .widget.row import Row
from .widget.footer import Footer

class App(Adw.Application):
    """Main application class."""

    def __init__(self):
        """Initialize the application and its components."""
        super().__init__(application_id="cloud.ivanbotty.Launcher")
        self.name = "Main Application"
        self.win = None

        # Create widgets
        self.listbox = Gtk.ListBox()
        self.listbox.set_visible(False)
        self.entry = SearchEntry(
            placeholder="Type to search...",
            width=UI_CONFS[PREFERENCES]["entry_width"],
            height=UI_CONFS[PREFERENCES]["entry_height"]
        )

        # Initialize services
        self.extensions_service = ExtensionService()
        try:
            # Load extensions from YAML
            with open("./cloud/ivanbotty/Launcher/resources/extensions.yaml") as f:
                config = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading extensions: {e}")
            return

        # Validate config structure
        if not isinstance(config, dict):
            print("Invalid extensions config format")
            return

        # Load extensions into the service
        self.extensions_service.load_from_config(config)

    def do_startup(self):
        """Startup routine for the application."""
        Gtk.Application.do_startup(self)
        print("Application startup")

        # Prepare services dictionary
        services = {
            ext.name.lower(): ext.service
            for ext in self.extensions_service.list_extensions()
            if ext.enabled
        }
        # Add the extensions service to the services dictionary
        services["extensions"] = self.extensions_service

        # Initialize controllers
        self.search_controller = SearchController(
            entry_widget=self.entry,
            listbox=self.listbox,
            services=services
        )

        # Adwaita setup
        Adw.init()
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)

        # Create main window
        self.win = Window(self)
        event_controller = KeyboardController(self)
        self.win.add_controller(event_controller)

        # Listbox setup
        self.listbox.set_visible(True)
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.set_vexpand(True)
        self.listbox.set_hexpand(True)

        # Create scrolled window for the listbox
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)
        scrolled_window.set_child(self.listbox)

        extensions_list = self.extensions_service.list_extensions()
        self.listbox.bind_model(extensions_list, self.create_row)

        # Create footer widget
        footer = Footer(self)

        # Layout setup
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_top(UI_CONFS[PREFERENCES]["margin_top"])
        box.set_margin_bottom(UI_CONFS[PREFERENCES]["margin_bottom"])
        box.set_margin_start(UI_CONFS[PREFERENCES]["margin_start"])
        box.set_margin_end(UI_CONFS[PREFERENCES]["margin_end"])
        box.append(self.entry)
        box.append(scrolled_window)
        box.append(footer)

        self.win.set_content(box)

    def create_row(self, app):
        """Create a row widget for the given app extension."""
        if getattr(app, "enabled", False):
            row = Row(app)
            row.app_model = app
            return row
        return None

    def do_activate(self):
        """Activate the application and show the window."""
        print("Application activated")
        if self.win is not None:
            self.win.present()