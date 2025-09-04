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
        If the text is empty, clears the view.
        Otherwise, finds a handler that can manage the text.
        """
        if not text.strip():
            self.view.set_child(None) if self.view.get_child() else None
            return
        for handler in self.handlers:
            if handler.can_handle(text):
                handler.handle(text, self.services, self.view)
                return
