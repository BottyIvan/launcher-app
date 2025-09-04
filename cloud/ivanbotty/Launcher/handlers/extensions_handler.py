from gi.repository import Gtk
import cloud.ivanbotty.Launcher.handlers.base_input_handler as bih
from cloud.ivanbotty.Launcher.widget import row as row_widget

class ExtensionHandler(bih.BaseInputHandler):
    def can_handle(self, text):
        # Anything that doesn't fit other handlers and doesn't start with >, ask, or http
        return False

    def handle(self, text, services, view):
        extensions_service = services.get("extensions")
        if extensions_service:
            listbox = Gtk.ListBox()
            listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
            listbox.add_css_class("boxed-list-separate")
            extensions_service.list_extensions()
            listbox.bind_model(extensions_service.list_extensions(), lambda ext: (
                row := row_widget.Row(ext),
                setattr(row, "extensions", ext),
                row
            ))
            view.set_child(listbox)
