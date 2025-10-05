from cloud.ivanbotty.Launcher.helper.load_class_instance import load_class_instance
import gi, yaml

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw

from cloud.ivanbotty.Launcher.services.extensions_service import ExtensionService
from cloud.ivanbotty.Launcher.controller.event_key_controller import EventKeyController
from cloud.ivanbotty.Launcher.controller.event_search_controller import EventSearchController
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES
from cloud.ivanbotty.Launcher.widget.window import Window
from cloud.ivanbotty.Launcher.widget.search_entry import SearchEntry
from cloud.ivanbotty.Launcher.widget.footer import Footer
from cloud.ivanbotty.Launcher.helper.thread_manager import ThreadManager

class App(Adw.Application):
    """Main application class."""

    def __init__(self):
        """Initialize the application and its components."""
        super().__init__(application_id="cloud.ivanbotty.Launcher")
        self.name = "Main Application"
        self.win = None

        # Create widgets
        self.view = Gtk.ListBox()
        self.view.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.view.add_css_class("boxed-list-separate")
        self.view.set_margin_start(UI_CONFS[PREFERENCES]["margin_start"])
        self.view.set_margin_end(UI_CONFS[PREFERENCES]["margin_end"])
        self.view.set_vexpand(True)
        self.view.set_hexpand(True)
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
            ext.name.lower(): load_class_instance(ext.service)
            for ext in self.extensions_service.list_extensions()
            if ext.enabled
        }

        # Prepare handlers dictionary
        handlers = {
            load_class_instance(ext.handler)
            for ext in self.extensions_service.list_extensions()
            if ext.enabled
        }

        # Initialize the search controller
        self.search_controller = EventSearchController(
            app=self,
            entry_widget=self.entry,
            view=self.view,
            services=services,
            handlers=handlers
        )

        # Load applications in the background at startup
        thread_manager = ThreadManager()
        apps_service = services.get("application")
        if apps_service:
            thread_manager.run_in_thread(apps_service.load_applications)

        # Adwaita setup
        Adw.init()
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)

        # Create main window
        self.win = Window(self)
        # Keyboard controller setup
        self.keyboard_controller = EventKeyController(self)
        self.win.add_controller(self.keyboard_controller)

        # Create scrolled window for the view
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)
        scrolled_window.set_child(self.view)

        # Create footer widget
        footer = Footer(self)

        # Layout setup
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.append(self.entry)
        box.append(scrolled_window)
        box.append(footer)

        self.win.set_content(box)

    def do_activate(self):
        """Activate the application and show the window."""
        print("Application activated")
        if self.win is not None:
            self.win.present()
