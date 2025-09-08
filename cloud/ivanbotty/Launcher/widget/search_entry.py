from gi.repository import Gtk, GObject
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES

class SearchEntry(Gtk.Entry):
    __gsignals__ = {
        "text-changed": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        "activated": (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }

    def __init__(self, placeholder="Type to search...", width=400, height=30):
        super().__init__()
        self.set_placeholder_text(placeholder)
        self.set_size_request(width, height)
        self.add_css_class("flat")
        self.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")
        self.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "edit-clear-symbolic")
        self.set_margin_start(UI_CONFS[PREFERENCES]["margin_start"])
        self.set_margin_end(UI_CONFS[PREFERENCES]["margin_end"])
        self.set_hexpand(True)

        # Connect internal signals
        self.connect("changed", self.on_changed)
        self.connect("activate", self.on_activate)

    def on_changed(self, entry):
        text = entry.get_text().strip()
        # Emit custom signal with trimmed text
        self.emit("text-changed", text)

    def on_activate(self, entry):
        text = entry.get_text().strip()
        # Emit custom signal with trimmed text
        self.emit("activated", text)
