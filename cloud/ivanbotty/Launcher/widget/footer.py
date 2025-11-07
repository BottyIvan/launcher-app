import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES
from cloud.ivanbotty.Launcher.widget.preferences import Preferences


class Footer(Adw.Bin):
    """Enhanced footer with improved keyboard shortcuts display.
    
    Features:
    - Modern visual design with better spacing
    - Clear keyboard shortcut hints
    - Preferences button with tooltip
    - Responsive layout
    """
    
    def __init__(self, app):
        super().__init__()
        self.app = app

        # Add CSS class for styling
        self.add_css_class("launcher-footer")

        # Create the main horizontal container for the footer
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.set_margin_start(UI_CONFS[PREFERENCES]["margin_start"])
        self.set_margin_end(UI_CONFS[PREFERENCES]["margin_end"])
        self.set_margin_top(8)
        self.set_margin_bottom(8)

        self.set_child(main_box)

        # Add the Preferences button to the left side
        preferences_btn = Gtk.Button()
        preferences_btn.set_valign(Gtk.Align.CENTER)
        preferences_btn.add_css_class("flat")
        preferences_btn.add_css_class("circular")
        preferences_icon = Adw.ButtonContent(
            icon_name="preferences-system-symbolic",
            label=""
        )
        preferences_btn.set_child(preferences_icon)
        preferences_btn.set_tooltip_text("Preferences (Ctrl+,)")
        preferences_btn.set_focus_on_click(False)
        preferences_btn.connect("clicked", lambda b: self.open_preferences())
        main_box.append(preferences_btn)

        # Add a spacer to push shortcut buttons to the right
        spacer = Gtk.Box(hexpand=True)
        main_box.append(spacer)

        # Define and add shortcut hints to the right side
        shortcut_definitions = [
            ("↑↓", "Navigate", "Use arrow keys to navigate through results"),
            ("↵", "Select", "Press Enter to launch the selected item"),
            ("Esc", "Close", "Press Escape to close the launcher"),
        ]
        
        for key_label, action_label, tooltip in shortcut_definitions:
            hint_box = self._create_shortcut_hint(key_label, action_label, tooltip)
            main_box.append(hint_box)

    def _create_shortcut_hint(self, key_label, action_label, tooltip):
        """Create a keyboard shortcut hint with key and action labels."""
        hint_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hint_box.set_valign(Gtk.Align.CENTER)
        hint_box.set_tooltip_text(tooltip)
        hint_box.add_css_class("shortcut-hint")
        
        # Key label with special styling
        key_lbl = Gtk.Label(label=key_label)
        key_lbl.add_css_class("monospace")
        key_lbl.add_css_class("dim-label")
        key_lbl.set_margin_start(8)
        key_lbl.set_margin_end(2)
        hint_box.append(key_lbl)
        
        # Action label
        action_lbl = Gtk.Label(label=action_label)
        action_lbl.add_css_class("caption")
        action_lbl.add_css_class("dim-label")
        action_lbl.set_margin_end(8)
        hint_box.append(action_lbl)
        
        return hint_box

    def open_preferences(self):
        """Open the preferences dialog."""
        Preferences(self.app).present()
