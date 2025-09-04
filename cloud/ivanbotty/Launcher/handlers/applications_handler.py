from gi.repository import Gtk
import cloud.ivanbotty.Launcher.handlers.base_input_handler as bih
from cloud.ivanbotty.Launcher.widget import row as row_widget

class AppHandler(bih.BaseInputHandler):
    def can_handle(self, text):
        # Anything that doesn't fit other handlers and doesn't start with >, ask, or http
        return True

    def handle(self, text, services, view):
        apps_service = services.get("application")
        if apps_service:
            listbox = Gtk.ListBox()
            listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
            listbox.add_css_class("boxed-list-separate")
            apps_service.load_applications()
            apps = apps_service.filter_applications(text)
            listbox.bind_model(apps, lambda app: row_widget.Row(app))
            view.set_child(listbox)
