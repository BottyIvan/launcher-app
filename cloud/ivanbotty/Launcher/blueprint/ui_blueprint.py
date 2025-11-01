"""
UI Blueprint - Central manager for UI creation.

Provides a high-level interface for creating complete UI layouts
and managing UI components using the blueprint design pattern.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw
from cloud.ivanbotty.Launcher.blueprint.style_blueprint import StyleBlueprint
from cloud.ivanbotty.Launcher.blueprint.component_registry import ComponentRegistry


class UIBlueprint:
    """
    Central UI management using blueprint design pattern.
    
    Coordinates style and component creation to build consistent,
    maintainable UI layouts throughout the application.
    """
    
    def __init__(self):
        """Initialize UI blueprint with style and component registry."""
        self.style = StyleBlueprint()
        self.components = ComponentRegistry(self.style)
    
    def create_window(self, app, title=None, resizable=False):
        """
        Create application window with blueprint styling.
        
        Args:
            app: Application instance
            title: Window title
            resizable: Whether window is resizable
            
        Returns:
            Adw.ApplicationWindow: Configured window
        """
        layout = self.style.get_layout()
        window = Adw.ApplicationWindow(application=app)
        window.set_default_size(layout['window_width'], layout['window_height'])
        window.set_resizable(resizable)
        
        if title:
            window.set_title(title)
        
        return window
    
    def create_search_bar(self, placeholder="Type to search..."):
        """
        Create standardized search bar with icons.
        
        Args:
            placeholder: Placeholder text
            
        Returns:
            Gtk.Entry: Search entry widget
        """
        entry = self.components.create_entry(
            placeholder=placeholder,
            icon_primary="system-search-symbolic",
            icon_secondary="edit-clear-symbolic",
            css_classes=["flat"]
        )
        
        layout = self.style.get_layout()
        self.style.apply_margins(entry, {
            'top': 0,
            'bottom': 0,
            'start': layout['margin_start'],
            'end': layout['margin_end']
        })
        
        return entry
    
    def create_main_list_view(self):
        """
        Create standardized main list view for results.
        
        Returns:
            Gtk.ListBox: Main list box widget
        """
        list_box = self.components.create_list_box(
            selection_mode=Gtk.SelectionMode.SINGLE,
            css_classes=["boxed-list-separate"],
            expand=True
        )
        
        layout = self.style.get_layout()
        self.style.apply_margins(list_box, {
            'top': 0,
            'bottom': 0,
            'start': layout['margin_start'],
            'end': layout['margin_end']
        })
        
        return list_box
    
    def create_footer_layout(self, app, shortcuts=None):
        """
        Create standardized footer layout.
        
        Args:
            app: Application instance
            shortcuts: List of (icon, description) tuples for shortcuts
            
        Returns:
            Adw.Bin: Footer widget
        """
        footer = Adw.Bin()
        layout = self.style.get_layout()
        
        main_box = self.components.create_box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing="lg"
        )
        
        self.style.apply_margins(footer, {
            'top': 0,
            'bottom': 0,
            'start': layout['margin_start'],
            'end': layout['margin_end']
        })
        footer.set_child(main_box)
        
        # Preferences button
        preferences_btn = self.components.create_icon_button(
            icon_name="applications-system-symbolic",
            tooltip="Open Preferences",
            css_classes=["flat"],
            on_click=lambda b: self._open_preferences(app)
        )
        preferences_btn.set_valign(Gtk.Align.CENTER)
        main_box.append(preferences_btn)
        
        # Spacer
        spacer = Gtk.Box(hexpand=True)
        main_box.append(spacer)
        
        # Shortcut buttons
        if shortcuts is None:
            shortcuts = [
                ("keyboard-enter-symbolic", "Select"),
                ("arrow1-down-symbolic", "Navigate Down"),
                ("arrow1-up-symbolic", "Navigate Up"),
            ]
        
        for icon_name, description in shortcuts:
            shortcut_btn = self.components.create_icon_button(
                icon_name=icon_name,
                tooltip=f"Press {icon_name.replace('-symbolic', '')} to {description}",
                css_classes=["flat"]
            )
            main_box.append(shortcut_btn)
        
        return footer
    
    def _open_preferences(self, app):
        """Open preferences dialog."""
        from cloud.ivanbotty.Launcher.widget.preferences import Preferences
        Preferences(app).present()
    
    def create_progress_bar(self, text="Loading..."):
        """
        Create standardized progress bar.
        
        Args:
            text: Progress text
            
        Returns:
            Gtk.ProgressBar: Configured progress bar
        """
        from cloud.ivanbotty.Launcher.widget.progress_bar import ProgressBar
        progress = ProgressBar(text)
        progress.set_visible(False)
        progress.set_hexpand(True)
        
        layout = self.style.get_layout()
        self.style.apply_margins(progress, {
            'top': layout.get('progress_margin_top', 6),
            'bottom': layout.get('progress_margin_bottom', 6),
            'start': layout['margin_start'],
            'end': layout['margin_end']
        })
        
        return progress
    
    def create_main_layout(self, entry, progress_bar, list_view, footer):
        """
        Create main application layout.
        
        Args:
            entry: Search entry widget
            progress_bar: Progress bar widget
            list_view: Main list view widget
            footer: Footer widget
            
        Returns:
            Gtk.Box: Main layout container
        """
        scrolled_window = self.components.create_scrolled_window(
            child=list_view,
            expand=True
        )
        
        layout = self.style.get_layout()
        main_box = self.components.create_box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing="md" if self.style.current_style == "default" else "sm",
            expand=False
        )
        
        main_box.append(entry)
        main_box.append(progress_bar)
        main_box.append(scrolled_window)
        main_box.append(footer)
        
        return main_box
    
    def create_list_row(self, app_model):
        """
        Create standardized list row for application.
        
        Args:
            app_model: Application model object
            
        Returns:
            Gtk.ListBoxRow: List row widget
        """
        from cloud.ivanbotty.Launcher.widget import row as row_widget
        return row_widget.Row(app_model)
    
    @staticmethod
    def initialize_theme():
        """Initialize Adwaita theme."""
        StyleBlueprint.init_adwaita_theme()
