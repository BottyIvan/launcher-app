import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
from cloud.ivanbotty.LightFlow.config.config import UI_CONFS, PREFERENCES
from cloud.ivanbotty.LightFlow.widget.preferences import Preferences


class Footer(Adw.Bin):
    """Footer with keyboard shortcuts display using native Adwaita styling."""
    
    def __init__(self, app):
        super().__init__()
        self.app = app

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

        # Add a spacer to push shortcut labels to the right
        spacer = Gtk.Box(hexpand=True)
        main_box.append(spacer)

        # Add shortcut labels with native styling
        shortcuts = [
            ("↑↓", "Navigate"),
            ("↵", "Select"),
            ("Esc", "Close"),
        ]
        
        for key_text, action_text in shortcuts:
            label = Gtk.Label(label=f"{key_text} {action_text}")
            label.add_css_class("dim-label")
            label.add_css_class("caption")
            label.set_valign(Gtk.Align.CENTER)
            main_box.append(label)

    def open_preferences(self):
        """Open the preferences dialog."""
        Preferences(self.app).present()
