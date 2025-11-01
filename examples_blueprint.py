#!/usr/bin/env python3
"""
Example implementation showing how to use Blueprint UI files with Gtk.Template.

This file demonstrates the recommended way to use the Blueprint UI files.
The existing widget classes can be migrated to this pattern over time.
"""

import gi
import os

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Example 1: Window with Template
@Gtk.Template(filename=os.path.join(PROJECT_ROOT, 'ui', 'main_window.ui'))
class TemplatedWindow(Adw.ApplicationWindow):
    """Example of using the main_window.blp template."""
    __gtype_name__ = 'LauncherWindow'
    
    # Bind template children using Gtk.Template.Child()
    # These match the IDs defined in the .blp/.ui file
    search_entry = Gtk.Template.Child()
    progress_box = Gtk.Template.Child()
    progress_bar = Gtk.Template.Child()
    list_view = Gtk.Template.Child()
    footer = Gtk.Template.Child()
    
    def __init__(self, application):
        super().__init__(application=application)
        # Template widgets are automatically initialized
        # You can now access them directly:
        # self.search_entry.set_text("example")
        # self.list_view.append(some_row)
        

# Example 2: SearchEntry with Template
@Gtk.Template(filename=os.path.join(PROJECT_ROOT, 'ui', 'search_entry.ui'))
class TemplatedSearchEntry(Gtk.Entry):
    """Example of using the search_entry.blp template."""
    __gtype_name__ = 'SearchEntry'
    
    def __init__(self):
        super().__init__()
        # Connect signals programmatically
        self.connect("changed", self.on_changed)
        self.connect("activate", self.on_activate)
    
    def on_changed(self, entry):
        text = entry.get_text().strip()
        print(f"Text changed: {text}")
    
    def on_activate(self, entry):
        text = entry.get_text().strip()
        print(f"Activated with: {text}")


# Example 3: ListBoxRow with Template
@Gtk.Template(filename=os.path.join(PROJECT_ROOT, 'ui', 'list_row.ui'))
class TemplatedRow(Gtk.ListBoxRow):
    """Example of using the list_row.blp template."""
    __gtype_name__ = 'LauncherRow'
    
    # Bind template children
    app_icon = Gtk.Template.Child()
    name_label = Gtk.Template.Child()
    desc_label = Gtk.Template.Child()
    tag_button = Gtk.Template.Child()
    
    def __init__(self, app_data):
        super().__init__()
        # Set data from app_data
        self.name_label.set_text(app_data.get("name", ""))
        
        # Set icon
        icon_name = app_data.get("icon", "application-x-addon-symbolic")
        from gi.repository import Gio
        gicon = Gio.ThemedIcon.new(icon_name)
        self.app_icon.set_from_gicon(gicon)
        
        # Set description if available
        desc = app_data.get("description", "")
        if desc:
            self.desc_label.set_text(desc)
            self.desc_label.set_visible(True)
        
        # Set tag if available
        tag = app_data.get("type", "")
        if tag:
            self.tag_button.set_label(tag)
            self.tag_button.set_visible(True)


# Example 4: Footer with Template
@Gtk.Template(filename=os.path.join(PROJECT_ROOT, 'ui', 'footer.ui'))
class TemplatedFooter(Adw.Bin):
    """Example of using the footer.blp template."""
    __gtype_name__ = 'LauncherFooter'
    
    # Bind template children
    preferences_btn = Gtk.Template.Child()
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        # Connect button signal
        self.preferences_btn.connect("clicked", self.on_preferences_clicked)
    
    def on_preferences_clicked(self, button):
        print("Opening preferences...")
        # Open preferences dialog
        # from cloud.ivanbotty.Launcher.widget.preferences import Preferences
        # Preferences(self.app).present()


# Example 5: Preferences with Template
@Gtk.Template(filename=os.path.join(PROJECT_ROOT, 'ui', 'preferences.ui'))
class TemplatedPreferences(Adw.PreferencesDialog):
    """Example of using the preferences.blp template."""
    __gtype_name__ = 'PreferencesDialog'
    
    # Bind template children
    compact_layout_switch = Gtk.Template.Child()
    gemini_api_key = Gtk.Template.Child()
    info_row = Gtk.Template.Child()
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        
        # Connect signals
        self.compact_layout_switch.connect("notify::active", self.on_layout_changed)
        self.gemini_api_key.connect("apply", self.on_api_key_apply)
        self.info_row.connect("activated", self.on_info_activated)
        
        # Load saved preferences
        # import cloud.ivanbotty.database.sqlite3 as db
        # self.compact_layout_switch.set_active(db.get_pref("layout", "default") == "compact")
        # self.gemini_api_key.set_text(db.get_api_key("gemini") or "")
    
    def on_layout_changed(self, switch, param):
        layout = "compact" if switch.get_active() else "default"
        print(f"Layout changed to: {layout}")
        # import cloud.ivanbotty.database.sqlite3 as db
        # db.set_pref("layout", layout)
    
    def on_api_key_apply(self, row):
        api_key = row.get_text().strip()
        if api_key:
            print(f"Saving API key...")
            # import cloud.ivanbotty.database.sqlite3 as db
            # db.set_api_key("gemini", api_key)
    
    def on_info_activated(self, row):
        print("Showing about dialog...")
        # Show about dialog
        # about = Adw.AboutDialog.new_from_appdata(...)
        # about.present()


if __name__ == "__main__":
    print("This file contains example implementations.")
    print("See the classes above for how to use Gtk.Template with Blueprint UI files.")
