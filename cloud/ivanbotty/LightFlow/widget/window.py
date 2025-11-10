import gi

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
from gi.repository import Adw, Gtk
from cloud.ivanbotty.LightFlow.config.config import UI_CONFS, PREFERENCES


class Window(Adw.ApplicationWindow):
    """Main window with keyboard shortcuts using native Adwaita styling.
    
    Features:
    - Responsive sizing with constraints
    - Keyboard shortcuts overlay (Ctrl+? or F1)
    - Native Adwaita look and feel
    """
    
    def __init__(self, application):
        super().__init__(application=application)
        
        # Window configuration
        width = UI_CONFS[PREFERENCES]["width"]
        height = UI_CONFS[PREFERENCES]["height"]
        self.set_default_size(width, height)
        
        # Allow resizing with minimum constraints
        self.set_resizable(True)
        self.set_size_request(600, 400)  # Minimum size
        
        # Set up keyboard shortcuts
        self._setup_shortcuts()
    
    def _setup_shortcuts(self):
        """Set up keyboard shortcuts and shortcuts overlay."""
        # Create shortcuts controller
        shortcut_ctrl = Gtk.ShortcutController()
        
        # Ctrl+? or F1 to show shortcuts window
        shortcut_help = Gtk.Shortcut.new(
            Gtk.ShortcutTrigger.parse_string("<Control>question"),
            Gtk.CallbackAction.new(self._show_shortcuts)
        )
        shortcut_ctrl.add_shortcut(shortcut_help)
        
        # F1 alternative
        shortcut_f1 = Gtk.Shortcut.new(
            Gtk.ShortcutTrigger.parse_string("F1"),
            Gtk.CallbackAction.new(self._show_shortcuts)
        )
        shortcut_ctrl.add_shortcut(shortcut_f1)
        
        # Ctrl+Q to quit
        shortcut_quit = Gtk.Shortcut.new(
            Gtk.ShortcutTrigger.parse_string("<Control>q"),
            Gtk.CallbackAction.new(lambda *args: self.close())
        )
        shortcut_ctrl.add_shortcut(shortcut_quit)
        
        # Ctrl+, for preferences
        shortcut_prefs = Gtk.Shortcut.new(
            Gtk.ShortcutTrigger.parse_string("<Control>comma"),
            Gtk.CallbackAction.new(self._show_preferences)
        )
        shortcut_ctrl.add_shortcut(shortcut_prefs)
        
        self.add_controller(shortcut_ctrl)
    
    def _show_shortcuts(self, *args):
        """Display the keyboard shortcuts overlay."""
        shortcuts_window = Gtk.ShortcutsWindow()
        shortcuts_window.set_transient_for(self)
        shortcuts_window.set_modal(True)
        
        # Create section
        section = Gtk.ShortcutsSection()
        section.set_property("section-name", "shortcuts")
        section.set_property("max-height", 10)
        
        # Navigation group
        nav_group = Gtk.ShortcutsGroup()
        nav_group.set_property("title", "Navigation")
        
        shortcuts_data = [
            ("Type", "Search applications and commands"),
            ("↑ / ↓", "Navigate results"),
            ("Enter", "Launch selected item"),
            ("Escape", "Close window"),
            ("Backspace", "Clear search"),
        ]
        
        for accel, desc in shortcuts_data:
            shortcut = Gtk.ShortcutsShortcut()
            shortcut.set_property("accelerator", accel)
            shortcut.set_property("title", desc)
            nav_group.append(shortcut)
        
        section.append(nav_group)
        
        # Application group
        app_group = Gtk.ShortcutsGroup()
        app_group.set_property("title", "Application")
        
        app_shortcuts = [
            ("<Control>comma", "Open preferences"),
            ("<Control>q", "Quit application"),
            ("<Control>question", "Show this help"),
            ("F1", "Show this help"),
        ]
        
        for accel, desc in app_shortcuts:
            shortcut = Gtk.ShortcutsShortcut()
            shortcut.set_property("accelerator", accel)
            shortcut.set_property("title", desc)
            app_group.append(shortcut)
        
        section.append(app_group)
        shortcuts_window.append(section)
        shortcuts_window.present()
        
        return True
    
    def _show_preferences(self, *args):
        """Show preferences dialog."""
        from cloud.ivanbotty.LightFlow.widget.preferences import Preferences
        Preferences(self.get_application()).present()
        return True
