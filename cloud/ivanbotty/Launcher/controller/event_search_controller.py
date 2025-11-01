from cloud.ivanbotty.Launcher.controller.event_base_controller import EventBaseController
from cloud.ivanbotty.Launcher.controller.event_click_controller import EventClickController
from cloud.ivanbotty.Launcher.widget import row as row_widget
import threading
import logging

logger = logging.getLogger(__name__)

class EventSearchController(EventBaseController):
    """Handles search and results, including mouse activations."""

    def __init__(self, app, entry_widget, view, services, handlers=None):
        super().__init__(app)
        self.entry = entry_widget
        self.view = view
        self.services = services
        self.handlers = handlers if handlers else []

        self.entry.connect("text-changed", self.on_text_changed)
        self.entry.connect("activated", self.on_activated)
        self.view.connect("row-activated", self.on_row_activated)

        self._debounce_timer = None

    def on_row_activated(self, listbox, row):
        """GTK callback: double click or Enter on a row."""
        self.activate_row(row)

    def on_text_changed(self, widget, text):
        if self._debounce_timer:
            self._debounce_timer.cancel()
        self._debounce_timer = threading.Timer(0.15, lambda: self.update_view(text))
        self._debounce_timer.start()

    def on_activated(self, widget, text):
        """GTK callback: Enter in the search entry."""
        for handler in self.handlers:
            if handler.can_handle(text):
                handler.handle(text, self.services, self.view)
                return
        logger.warning(f"No handler found for text: {text}")

    def update_view(self, text):
        """Update the ListBox based on the results returned by handlers."""
        for handler in self.handlers:
            if handler.can_handle(text):
                if list_model := handler.handle(text, self.services):
                    self.view.bind_model(list_model, lambda row_item: (
                        row := row_widget.Row(row_item),
                        setattr(row, "item_model", row_item),
                        EventClickController(self.app, row),
                        row
                    ))
