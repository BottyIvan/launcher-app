import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk

from cloud.ivanbotty.Launcher.controller.event_base_controller import EventBaseController

class EventKeyController(EventBaseController, Gtk.EventControllerKey):
    """Handles keyboard events (Enter, Escape, arrows, Backspace)."""

    def __init__(self, app):
        EventBaseController.__init__(self, app)
        Gtk.EventControllerKey.__init__(self)
        self.connect("key-pressed", self.on_key_pressed)

    def on_key_pressed(self, controller, keyval, keycode, state):
        actions = {
            Gdk.KEY_BackSpace: self.reset_search,
            Gdk.KEY_Escape: self.app.win.close,
            Gdk.KEY_Return: self.activate_selected_row,
            Gdk.KEY_Down: lambda: self.scroll_list("down"),
            Gdk.KEY_Up: lambda: self.scroll_list("up"),
        }
        if action := actions.get(keyval):
            action()
            return True
        return False

    def activate_selected_row(self):
        """Activates the currently selected row in the ListBox."""
        row = self.app.view.get_selected_row()
        self.activate_row(row)

    def scroll_list(self, direction):
        """Focuses the first child of the ListBox when using arrow keys."""
        child = self.app.view.get_first_child()
        if child:
            child.grab_focus()

    def reset_search(self):
        """Clears the search entry and focuses it."""
        self.app.entry.set_text("")
        self.app.entry.grab_focus()
