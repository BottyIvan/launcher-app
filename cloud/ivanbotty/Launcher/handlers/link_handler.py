import re
from gi.repository import Gio, Gtk
import cloud.ivanbotty.Launcher.handlers.base_input_handler as bih


class LinkHandler(bih.BaseInputHandler):
    def can_handle(self, text):
        return re.match(r"^https?://", text.strip())

    def handle(self, text, services, listbox):
        try:
            Gio.AppInfo.launch_default_for_uri(text, None)
            listbox.remove_all()
            listbox.insert(Gtk.Label(label=f"Opening link: {text}"), 0)
        except Exception as e:
            listbox.remove_all()
            listbox.insert(Gtk.Label(label=f"Cannot open link: {e}"), 0)
