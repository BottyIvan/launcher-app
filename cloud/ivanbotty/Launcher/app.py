from cloud.ivanbotty.Launcher.helper.load_class_instance import load_class_instance
import gi, yaml

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, GLib

from cloud.ivanbotty.Launcher.services.extensions_service import ExtensionService
from cloud.ivanbotty.Launcher.controller.event_key_controller import EventKeyController
from cloud.ivanbotty.Launcher.controller.event_search_controller import EventSearchController
from cloud.ivanbotty.Launcher.widget.search_entry import SearchEntry
from cloud.ivanbotty.Launcher.helper.thread_manager import ThreadManager
from cloud.ivanbotty.Launcher.blueprint import UIBlueprint

class App(Adw.Application):
    """Main application class."""

    def __init__(self):
        """Initialize the application and its components."""
        super().__init__(application_id="cloud.ivanbotty.Launcher")
        self.name = "Main Application"
        self.win = None

        # Initialize UI blueprint for consistent component creation
        self.ui_blueprint = UIBlueprint()

        # Create widgets using blueprint
        self.progress_bar = self.ui_blueprint.create_progress_bar("Loading...")
        self.view = self.ui_blueprint.create_main_list_view()
        self.entry = SearchEntry(ui_blueprint=self.ui_blueprint)

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

    def run_with_progress(self, target_func, steps=100, delay=0.02, text="Processing..."):
        """Executes a function while displaying the progress bar during the process."""
        self.progress_bar.set_text(text)
        self.progress_bar.set_fraction(0.0)
        self.progress_bar.set_visible(True)
        def wrapper():
            self.progress_bar.start_long_task(steps=steps, delay=delay)
            target_func()
            GLib.idle_add(self.progress_bar.set_visible, False)
        ThreadManager().run_in_thread(wrapper)

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
        apps_service = services.get("application")
        if apps_service:
            self.run_with_progress(apps_service.load_applications, text="Loading applications...")

        # Initialize Adwaita theme using blueprint
        self.ui_blueprint.initialize_theme()

        # Create main window using blueprint
        self.win = self.ui_blueprint.create_window(self)
        
        # Keyboard controller setup
        self.keyboard_controller = EventKeyController(self)
        self.win.add_controller(self.keyboard_controller)

        # Create footer widget using blueprint
        footer = self.ui_blueprint.create_footer_layout(self)

        # Create main layout using blueprint
        main_layout = self.ui_blueprint.create_main_layout(
            self.entry,
            self.progress_bar,
            self.view,
            footer
        )

        self.win.set_content(main_layout)

    def do_activate(self):
        """Activate the application and show the window."""
        print("Application activated")
        if self.win is not None:
            self.win.present()
