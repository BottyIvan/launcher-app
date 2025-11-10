import gi
import logging

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

logger = logging.getLogger(__name__)


class EventBaseController:
    """Base controller for common management of rows and results."""

    def __init__(self, app):
        self.app = app

    def activate_row(self, row):
        """Common logic to activate a result (Enter, double click, etc.)."""
        if not isinstance(row, Gtk.ListBoxRow):
            return

        item_model = getattr(row, "item_model", None)
        if callable(getattr(item_model, "run", None)):
            try:
                item_model.run()
            except Exception as e:
                logger.error(f"Error running item_model: {e}")
            finally:
                if hasattr(self.app.win, "close"):
                    self.app.win.close()
