from gi.repository import Gtk, GObject

class SearchEntry(Gtk.Entry):
    __gsignals__ = {
        "text-changed": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        "activated": (GObject.SignalFlags.RUN_FIRST, None, (str,))
    }

    def __init__(self, placeholder="Type to search...", width=None, height=None, ui_blueprint=None):
        super().__init__()
        self.set_placeholder_text(placeholder)
        
        # Use blueprint if provided, otherwise use legacy parameters
        if ui_blueprint:
            layout = ui_blueprint.style.get_layout()
            width = width or layout['entry_width']
            height = height or layout['entry_height']
            margin_start = layout['margin_start']
            margin_end = layout['margin_end']
        else:
            # Fallback to config for legacy support
            from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES
            width = width or UI_CONFS[PREFERENCES]["entry_width"]
            height = height or UI_CONFS[PREFERENCES]["entry_height"]
            margin_start = UI_CONFS[PREFERENCES]["margin_start"]
            margin_end = UI_CONFS[PREFERENCES]["margin_end"]
        
        self.set_size_request(width, height)
        self.add_css_class("flat")
        self.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")
        self.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "edit-clear-symbolic")
        self.set_margin_start(margin_start)
        self.set_margin_end(margin_end)
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
