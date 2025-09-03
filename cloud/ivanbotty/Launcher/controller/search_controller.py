from cloud.ivanbotty.Launcher.widget.row import Row

class SearchController:
    def __init__(self, entry_widget, listbox, services, handlers=[]):
        """
        entry_widget: Gtk.SearchEntry
        listbox: Gtk.ListBox
        services: dict of available services
        handlers: list of registered handlers
        """
        self.entry = entry_widget
        self.listbox = listbox
        self.services = services
        self.handlers = handlers

        self.entry.connect("text-changed", self.on_text_changed)
        self.entry.connect("activated", self.on_activated)

    def on_text_changed(self, widget, text):
        self.update_listbox(text)

    def on_activated(self, widget, text):
        for handler in self.handlers:
            if handler.can_handle(text):
                handler.handle(text, self.services, self.listbox)
                return
        print("No handler found for:", text)

    def update_listbox(self, text):
        self.listbox.remove_all()
        if not text.strip():
            extensions_list = self.services["extensions"].list_extensions()
            self.listbox.bind_model(extensions_list, self.create_row_for_extension)
            return
        for handler in self.handlers:
            if handler.can_handle(text):
                handler.handle(text, self.services, self.listbox)
                return

    def create_row_for_extension(self, app):
        if getattr(app, "enabled", False):
            from cloud.ivanbotty.Launcher.widget.row import Row
            row = Row(app)
            row.app_model = app
            return row
        return None
