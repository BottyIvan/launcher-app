import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, GObject
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES


class SearchEntry(Gtk.Entry):
    """Enhanced search entry with modern styling and better UX.
    
    Features:
    - Modern visual design with rounded corners and shadows
    - Clear button that appears when text is entered
    - Smooth transitions and hover effects
    - Improved icon positioning
    """
    
    __gsignals__ = {
        "text-changed": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        "activated": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self, placeholder="Type to search...", width=400, height=30):
        super().__init__()
        self.set_placeholder_text(placeholder)
        self.set_size_request(width, height)
        
        # Apply modern styling classes
        self.add_css_class("search-entry")
        self.add_css_class("flat")
        
        # Configure icons with better visual hierarchy
        self.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")
        self.set_icon_activatable(Gtk.EntryIconPosition.PRIMARY, False)
        
        # Clear icon only shows when there's text
        self._update_clear_icon()
        
        # Set margins and expansion
        self.set_margin_start(UI_CONFS[PREFERENCES]["margin_start"])
        self.set_margin_end(UI_CONFS[PREFERENCES]["margin_end"])
        self.set_margin_top(UI_CONFS[PREFERENCES].get("margin_top", 16))
        self.set_hexpand(True)

        # Connect internal signals
        self.connect("changed", self.on_changed)
        self.connect("activate", self.on_activate)
        self.connect("icon-press", self.on_icon_press)

    def _update_clear_icon(self):
        """Show or hide clear icon based on whether there's text."""
        text = self.get_text()
        if text:
            self.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "edit-clear-symbolic")
            self.set_icon_activatable(Gtk.EntryIconPosition.SECONDARY, True)
        else:
            self.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)
            self.set_icon_activatable(Gtk.EntryIconPosition.SECONDARY, False)

    def on_icon_press(self, entry, icon_pos):
        """Handle icon press - clear text when secondary icon is clicked."""
        if icon_pos == Gtk.EntryIconPosition.SECONDARY:
            self.set_text("")
            self.grab_focus()

    def on_changed(self, entry):
        text = entry.get_text().strip()
        self._update_clear_icon()
        # Emit custom signal with trimmed text
        self.emit("text-changed", text)

    def on_activate(self, entry):
        text = entry.get_text().strip()
        # Emit custom signal with trimmed text
        self.emit("activated", text)
