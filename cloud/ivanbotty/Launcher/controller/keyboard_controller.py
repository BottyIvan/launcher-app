import gi,subprocess
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk

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
        return self.reset_search()

    def scroll_list(self, direction):
        self.app.listbox.get_first_child().grab_focus()

    def confirm_selection(self):
        selected_row = self.app.listbox.get_selected_row()
        if selected_row:
            # Assuming each row's child is a widget that has an ApplicationModel attached
            app_model = getattr(selected_row, "app_model", None)
            if app_model and hasattr(app_model, "exec_cmd"):
                exec_cmd = app_model.exec_cmd
                print("Selected app exec_cmd:", exec_cmd)
                # You can run the command if needed:
                if (subprocess.Popen(exec_cmd, shell=True)):
                    self.app.win.close()
            else:
                print("No ApplicationModel attached to selected row.")
        else:
            print("No row selected.")

    def reset_search(self):
        self.app.entry.set_text("")
        self.app.entry.grab_focus()