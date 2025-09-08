import gi

from cloud.ivanbotty.Launcher.models.applications_model import ApplicationModel
gi.require_version("Gtk", "4.0")
from cloud.ivanbotty.Launcher.widget import row as row_widget

class SearchController:
    def __init__(self, entry_widget, view, services, handlers=None):
        """
        Initializes the search controller.

        Args:
            entry_widget: Gtk.SearchEntry, the search input widget.
            view: Adw.Bin, the container view where results are displayed.
            services: dict, dictionary of available services.
            handlers: list, list of registered handlers to manage the search.
        """
        self.entry = entry_widget
        self.view = view
        self.services = services
        self.handlers = handlers if handlers is not None else []

        # Connect the search widget signals to the controller methods
        self.entry.connect("text-changed", self.on_text_changed)
        self.entry.connect("activated", self.on_activated)

    def on_text_changed(self, widget, text):
        """
        Called when the search text changes.
        Updates the view based on the new text.
        """
        self.update_view(text)

    def on_activated(self, widget, text):
        """
        Called when the search is activated (e.g., pressing Enter).
        Finds a handler that can manage the text and executes it.
        """
        for handler in self.handlers:
            if handler.can_handle(text):
                handler.handle(text, self.services, self.view)
                return
        print("No handler found for:", text)

    def update_view(self, text):
        """
        Updates the view based on the search text.

        - If the text is empty or no handler can process it, the view remains unchanged.
        - If a handler can process the text, it retrieves a model of results and binds it to the view.
        - For each item in the model, a custom row widget is created and its type is set.
        - Prints the name of each item in the model for debugging purposes.
        """
        for handler in self.handlers:
            if handler.can_handle(text):
                # Handler returns a list model of results for the given text
                if list_model := handler.handle(text, self.services):
                    # Bind the model to the view, creating a row widget for each item
                    self.view.bind_model(list_model, lambda row_item: (
                        row := row_widget.Row(row_item),
                        setattr(row, "item_model", row_item),
                        row
                    ))
