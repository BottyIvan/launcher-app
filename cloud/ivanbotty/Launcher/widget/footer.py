import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES
from cloud.ivanbotty.Launcher.widget.preferences import Preferences


class Footer(Adw.Bin):
    def __init__(self, app):
        super().__init__()
        self.app = app

        # Create the main horizontal container for the footer
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.set_margin_start(UI_CONFS[PREFERENCES]["margin_start"])
        self.set_margin_end(UI_CONFS[PREFERENCES]["margin_end"])

        self.set_child(main_box)

        # Add the Preferences button to the left side
        preferences_btn = Gtk.Button()
        preferences_btn.set_valign(Gtk.Align.CENTER)
        preferences_btn.add_css_class("flat")
        preferences_icon = Adw.ButtonContent(icon_name="applications-system-symbolic")
        preferences_btn.set_child(preferences_icon)
        preferences_btn.set_tooltip_text("Open Preferences")
        preferences_btn.set_focus_on_click(False)
        preferences_btn.connect("clicked", lambda b: self.open_preferences())
        main_box.append(preferences_btn)

        # Add a spacer to push shortcut buttons to the right
        spacer = Gtk.Box(hexpand=True)
        main_box.append(spacer)

        # Define and add shortcut buttons to the right side
        shortcut_definitions = [
            ("keyboard-enter-symbolic", "Select"),
            ("arrow1-down-symbolic", "Navigate Down"),
            ("arrow1-up-symbolic", "Navigate Up"),
        ]
        for icon_name, description in shortcut_definitions:
            shortcut_btn = Gtk.Button()
            shortcut_icon = Adw.ButtonContent(icon_name=icon_name)
            shortcut_btn.set_child(shortcut_icon)
            shortcut_btn.add_css_class("flat")
            shortcut_btn.set_tooltip_text(
                f"Press {icon_name} to {description}" if description else f"Press {icon_name}"
            )
            main_box.append(shortcut_btn)

    def open_preferences(self):
        # Import and present the Preferences window
        Preferences(self.app).present()
