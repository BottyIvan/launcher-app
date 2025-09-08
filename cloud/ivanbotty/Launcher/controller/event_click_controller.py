import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .event_base_controller import EventBaseController

class EventClickController(EventBaseController):
    """Handles click/double-click events on a row or widget."""

    def __init__(self, app, widget):
        """
        widget: the widget on which to capture clicks (e.g., a ListBox Row)
        """
        super().__init__(app)

        self.widget = widget
        gesture = Gtk.GestureClick.new()
        gesture.set_button(0)  # 0 = any button
        gesture.connect("pressed", self.on_pressed)
        self.widget.add_controller(gesture)

    def on_pressed(self, gesture, n_press, x, y):
        """GTK callback: executed on every click on the widget."""
        if n_press == 2:  # double click
            self.activate_row(self.widget)
