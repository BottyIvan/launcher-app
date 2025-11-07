"""Main Launcher application.

This module provides the main GTK4/Adwaita application for the Launcher,
handling UI setup, extension management, and search functionality.
"""

import logging
from typing import Optional

import gi
import yaml

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GLib, Gtk, Gdk

from cloud.ivanbotty.Launcher.config.config import PREFERENCES, UI_CONFS
from cloud.ivanbotty.Launcher.controller.event_key_controller import EventKeyController
from cloud.ivanbotty.Launcher.controller.event_search_controller import (
    EventSearchController,
)
from cloud.ivanbotty.Launcher.helper.load_class_instance import load_class_instance
from cloud.ivanbotty.Launcher.helper.thread_manager import ThreadManager
from cloud.ivanbotty.Launcher.services.extensions_service import ExtensionService
from cloud.ivanbotty.Launcher.widget.footer import Footer
from cloud.ivanbotty.Launcher.widget.progress_bar import ProgressBar
from cloud.ivanbotty.Launcher.widget.search_entry import SearchEntry
from cloud.ivanbotty.Launcher.widget.window import Window
from cloud.ivanbotty.common import find_extensions_yaml

logger = logging.getLogger(__name__)


class App(Adw.Application):
    """Main Launcher application class.

    Attributes:
        name: Application name
        win: Main application window
        progress_bar: Progress indicator widget
        view: ListBox for displaying search results
        entry: Search entry widget
        extensions_service: Service for managing extensions
        search_controller: Controller for handling search events
        keyboard_controller: Controller for handling keyboard events
    """

    def __init__(self, app: str) -> None:
        """Initialize the application and its components.

        Args:
            app: Application ID string
        """
        super().__init__(application_id=app)
        self.name = "Main Application"
        self.win: Optional[Window] = None

        # Initialize progress bar with configuration
        self.progress_bar = ProgressBar("Loading...")
        self.progress_bar.set_visible(False)
        self.progress_bar.set_margin_top(UI_CONFS[PREFERENCES].get("progress_margin_top", 6))
        self.progress_bar.set_margin_bottom(UI_CONFS[PREFERENCES].get("progress_margin_bottom", 6))
        self.progress_bar.set_margin_start(UI_CONFS[PREFERENCES]["margin_start"])
        self.progress_bar.set_margin_end(UI_CONFS[PREFERENCES]["margin_end"])
        self.progress_bar.set_hexpand(True)

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
            height=UI_CONFS[PREFERENCES]["entry_height"],
        )

        # Initialize services
        self.extensions_service = ExtensionService()
        try:
            yaml_path = find_extensions_yaml("extensions.yaml")
            if yaml_path is None:
                logger.error("extensions.yaml file not found")
                return
            with open(yaml_path) as f:
                config = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading extensions: {e}")
            return

        # Validate config structure
        if not isinstance(config, dict):
            logger.error("Invalid extensions config format")
            return

        # Load extensions into the service
        self.extensions_service.load_from_config(config)

    def run_with_progress(
        self,
        target_func: callable,
        steps: int = 100,
        delay: float = 0.02,
        text: str = "Processing...",
    ) -> None:
        """Execute a function while displaying the progress bar.

        Args:
            target_func: Function to execute
            steps: Number of progress steps
            delay: Delay between steps in seconds
            text: Text to display on progress bar
        """
        self.progress_bar.set_text(text)
        self.progress_bar.set_fraction(0.0)
        self.progress_bar.set_visible(True)

        def wrapper():
            self.progress_bar.start_long_task(steps=steps, delay=delay)
            target_func()
            GLib.idle_add(self.progress_bar.set_visible, False)

        ThreadManager().run_in_thread(wrapper)

    def do_startup(self) -> None:
        """Perform startup routine for the application."""
        Gtk.Application.do_startup(self)
        logger.info("Application startup")

        # Load custom CSS for modern UI
        self._load_custom_css()

        # Prepare services dictionary
        services = {
            ext.name.lower(): load_class_instance(ext.service)
            for ext in self.extensions_service.list_extensions()
            if ext.enabled
        }

        # Prepare handlers set and check for None handlers
        handlers = {
            h for ext in self.extensions_service.list_extensions()
            if ext.enabled
            if (h := load_class_instance(ext.handler)) is not None
        }

        # Initialize the search controller
        self.search_controller = EventSearchController(
            app=self, entry_widget=self.entry, view=self.view, services=services, handlers=handlers
        )

        # Load applications in the background at startup
        apps_service = services.get("application")
        if apps_service:
            self.run_with_progress(apps_service.load_applications, text="Loading applications...")

        # Adwaita setup
        Adw.init()
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)

        # Create main window
        self.win = Window(self)

        # Keyboard controller setup
        self.keyboard_controller = EventKeyController(self)
        self.win.add_controller(self.keyboard_controller)

        # Create scrolled window for the view with styling
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)
        scrolled_window.add_css_class("results-list")
        scrolled_window.set_child(self.view)

        # Create footer widget
        footer = Footer(self)

        # Layout setup with CSS classes
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.add_css_class("launcher-content")
        box.append(self.entry)
        box.append(self.progress_bar)
        box.append(scrolled_window)
        box.append(footer)

        self.win.set_content(box)

    def _load_custom_css(self) -> None:
        """Load custom CSS stylesheet for modern UI styling."""
        try:
            css_provider = Gtk.CssProvider()
            css_provider.load_from_resource("/cloud/ivanbotty/Launcher/resources/style.css")
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
            logger.info("Custom CSS loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load custom CSS: {e}")

    def do_activate(self) -> None:
        """Activate the application and show the window."""
        logger.info("Application activated")
        if self.win is not None:
            self.win.present()
