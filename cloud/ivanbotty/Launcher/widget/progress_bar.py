import threading
import time
from gi.repository import Gtk, GLib


class ProgressBar(Gtk.ProgressBar):
    def __init__(self, text="Loading..."):
        """Initialize the ProgressBar with optional display text."""
        super().__init__()
        self.set_show_text(True)
        self.set_text(text)
        self.set_fraction(0.0)
        
        # Add CSS classes for modern styling
        self.add_css_class("launcher-progress")

    def update_progress(self, fraction, text=None):
        """
        Update the progress bar fraction and optionally the display text.
        Ensures fraction is between 0.0 and 1.0.
        Uses GLib.idle_add to safely update the UI from any thread.
        """
        fraction = max(0.0, min(1.0, fraction))
        percent = int(fraction * 100)
        display_text = f"{text} {percent}%" if text else f"{percent}%"
        GLib.idle_add(self._set_progress, fraction, display_text, priority=GLib.PRIORITY_DEFAULT)

    def _set_progress(self, fraction, display_text):
        """
        Internal method to set the progress bar fraction and text.
        Called in the main GTK thread.
        """
        self.set_fraction(fraction)
        self.set_text(display_text)
        return False  # Remove the idle handler after execution

    def start_long_task(self, steps=100, delay=0.05, text="Loading..."):
        """
        Simulate a long-running task by updating the progress bar in a separate thread.
        'steps' defines the number of increments, 'delay' is the time between updates.
        """

        def task():
            for i in range(steps + 1):
                self.update_progress(i / steps, text)
                time.sleep(delay)

        threading.Thread(target=task, daemon=True).start()
