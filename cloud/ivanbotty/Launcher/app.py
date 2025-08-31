import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gio

from .services.applications_service import ApplicationsService
from .controller.keyboard_controller import KeyboardController
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES
from .widget.window import Window
from .widget.row import Row
from .widget.footer import Footer

class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id="cloud.ivanbotty.Launcher")
        self.name = "Main Application"

        self.win = None
        self.listbox = Gtk.ListBox()
        self.listbox.set_visible(False)
        self.entry = None

        # Load applications at startup
        self.applications_service = ApplicationsService()
        self.applications_service.load_applications()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        print("Application startup")

        Adw.init()
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)

        self.win = Window(self)
        event_controller = KeyboardController(self)
        self.win.add_controller(event_controller)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Search app or file…")
        self.entry.connect("changed", self.on_entry_changed)
        self.entry.set_size_request(UI_CONFS[PREFERENCES]["entry_width"], UI_CONFS[PREFERENCES]["entry_height"])

        self.listbox.set_visible(True)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)
        scrolled_window.set_child(self.listbox)

        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.set_vexpand(True)
        self.listbox.set_hexpand(True)

        # Show all apps at startup
        filtered_store = self.applications_service.filter_applications("")
        self.listbox.bind_model(filtered_store, lambda app: self.create_row(app))

        footer = Footer()

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
        row = Row(app)
        row.app_model = app
        return row

    def do_activate(self):
        print("Application activated")
        if self.win is not None:
            self.win.present()

    def on_entry_changed(self, entry):
        search_text = entry.get_text().lower()
        filtered_store = self.applications_service.filter_applications(search_text)
        self.listbox.bind_model(filtered_store, lambda app: self.create_row(app))