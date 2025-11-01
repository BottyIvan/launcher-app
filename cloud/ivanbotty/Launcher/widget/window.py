import gi
gi.require_version("Adw", "1")
from gi.repository import Adw
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES

class Window(Adw.ApplicationWindow):
    """Main application window.
    
    This class can be updated to use Gtk.Template with ui/main_window.ui
    when the Blueprint transition is complete.
    """
    def __init__(self, application):
        super().__init__(application=application)
        self.set_default_size(UI_CONFS[PREFERENCES]["width"], UI_CONFS[PREFERENCES]["height"])
        self.set_resizable(False)
