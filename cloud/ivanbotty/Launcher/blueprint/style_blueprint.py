"""
Style Blueprint - Centralized styling and theming configuration.

Provides a single source of truth for all UI styling, spacing, and theming
to ensure consistency across the application.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw


class StyleBlueprint:
    """
    Centralized style management for the application.
    
    Provides consistent spacing, sizing, and theming values
    that can be applied to any widget.
    """
    
    # Style presets
    COMPACT = "compact"
    DEFAULT = "default"
    
    # Spacing values
    SPACING = {
        "none": 0,
        "xs": 2,
        "sm": 4,
        "md": 8,
        "lg": 12,
        "xl": 16,
        "xxl": 24
    }
    
    # Size presets
    SIZES = {
        "icon_xs": 16,
        "icon_sm": 24,
        "icon_md": 28,
        "icon_lg": 32,
        "icon_xl": 48
    }
    
    # Layout configurations
    LAYOUTS = {
        COMPACT: {
            "window_width": 700,
            "window_height": 400,
            "entry_width": 660,
            "entry_height": 36,
            "margin_top": 8,
            "margin_bottom": 8,
            "margin_start": 8,
            "margin_end": 8,
            "row_spacing": 6,
            "progress_margin_top": 6,
            "progress_margin_bottom": 6
        },
        DEFAULT: {
            "window_width": 800,
            "window_height": 540,
            "entry_width": 760,
            "entry_height": 48,
            "margin_top": 16,
            "margin_bottom": 16,
            "margin_start": 16,
            "margin_end": 16,
            "row_spacing": 8,
            "progress_margin_top": 6,
            "progress_margin_bottom": 6
        }
    }
    
    def __init__(self, preference_loader=None):
        """
        Initialize style blueprint with current theme preferences.
        
        Args:
            preference_loader: Optional callable that returns (key, default) -> value
                              If None, uses default database loader
        """
        self._preference_loader = preference_loader or self._default_preference_loader
        self._current_style = self._load_style_preference()
    
    def _default_preference_loader(self, key, default):
        """Default preference loader using database module."""
        try:
            import cloud.ivanbotty.database.sqlite3 as db
            return db.get_pref(key, default)
        except Exception:
            return default
    
    def _load_style_preference(self):
        """Load style preference from configured loader."""
        try:
            pref = self._preference_loader("layout", self.DEFAULT)
            return pref if pref in self.LAYOUTS else self.DEFAULT
        except Exception:
            return self.DEFAULT
    
    @property
    def current_style(self):
        """Get the current active style."""
        return self._current_style
    
    def get_layout(self, style=None):
        """
        Get layout configuration for a specific style.
        
        Args:
            style: Style name (COMPACT or DEFAULT), uses current if None
            
        Returns:
            dict: Layout configuration
        """
        style = style or self._current_style
        return self.LAYOUTS.get(style, self.LAYOUTS[self.DEFAULT])
    
    def apply_margins(self, widget, margins=None):
        """
        Apply standard margins to a widget.
        
        Args:
            widget: GTK widget to apply margins to
            margins: dict with 'top', 'bottom', 'start', 'end' keys or None for defaults
        """
        layout = self.get_layout()
        if margins is None:
            margins = {
                'top': layout['margin_top'],
                'bottom': layout['margin_bottom'],
                'start': layout['margin_start'],
                'end': layout['margin_end']
            }
        
        widget.set_margin_top(margins.get('top', layout['margin_top']))
        widget.set_margin_bottom(margins.get('bottom', layout['margin_bottom']))
        widget.set_margin_start(margins.get('start', layout['margin_start']))
        widget.set_margin_end(margins.get('end', layout['margin_end']))
    
    def apply_spacing(self, box, spacing_name="md"):
        """
        Apply consistent spacing to a box container.
        
        Args:
            box: GTK Box widget
            spacing_name: Spacing preset name (xs, sm, md, lg, xl, xxl)
        """
        spacing = self.SPACING.get(spacing_name, self.SPACING["md"])
        box.set_spacing(spacing)
    
    def get_icon_size(self, size_name="md"):
        """
        Get standard icon size.
        
        Args:
            size_name: Size preset name (xs, sm, md, lg, xl)
            
        Returns:
            int: Icon pixel size
        """
        return self.SIZES.get(f"icon_{size_name}", self.SIZES["icon_md"])
    
    def apply_css_classes(self, widget, classes):
        """
        Apply multiple CSS classes to a widget.
        
        Args:
            widget: GTK widget
            classes: List of CSS class names or single class name string
        """
        if isinstance(classes, str):
            classes = [classes]
        for css_class in classes:
            widget.add_css_class(css_class)
    
    @staticmethod
    def init_adwaita_theme():
        """Initialize Adwaita theme with default color scheme."""
        Adw.init()
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)
