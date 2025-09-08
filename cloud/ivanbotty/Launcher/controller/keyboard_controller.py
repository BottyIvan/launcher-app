import gi,subprocess
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GObject

class KeyboardController(Gtk.EventControllerKey):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.connect("key-pressed", self.on_key_pressed)

    def on_key_pressed(self, controller, keyval, keycode, state):
        actions = {
            Gdk.KEY_BackSpace: lambda: self.reset_search(),
            Gdk.KEY_Escape: self.app.win.close,
            Gdk.KEY_Return: lambda: self.confirm_selection(),
            Gdk.KEY_Down: lambda: self.scroll_list("down"),
            Gdk.KEY_Up: lambda: self.scroll_list("up"),
        }
        action = actions.get(keyval)
        if action:
            action()
            return True  # Event handled
        return False  # Event not handled

    def scroll_list(self, direction):
        # Focus the first child of the list when scrolling
        self.app.view.get_first_child().grab_focus()

    def confirm_selection(self):
        # Get the currently selected row from the view
        selected_row = self.app.view.get_selected_row()
        if not isinstance(selected_row, Gtk.ListBoxRow):
            return

        # Retrieve the item_model attribute from the selected row
        item_model = getattr(selected_row, "item_model", None)
        # If item_model has a callable 'run' method, execute it
        if callable(getattr(item_model, "run", None)):
            try:
                item_model.run()
            except Exception as e:
                # Print any error that occurs during execution
                print(f"Error running item_model: {e}")
            finally:
                # Close the application window after execution
                self.app.win.close()

    def reset_search(self):
        self.app.entry.set_text("")
        self.app.entry.grab_focus()