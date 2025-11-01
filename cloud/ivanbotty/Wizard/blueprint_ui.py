"""
Blueprint UI loader and window components for the Wizard module.

This module provides classes to load and manage UI components
compiled from GNOME Blueprint (.blp) files.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio
import logging

logger = logging.getLogger(__name__)


class WizardWindowBlueprint(Adw.ApplicationWindow):
    """
    Main wizard window loaded from Blueprint UI.
    
    This class loads the wizard-window.ui file compiled from
    wizard-window.blp and provides access to the carousel and
    indicator widgets.
    """
    
    def __init__(self, application=None):
        super().__init__(application=application)
        
        # Load UI from GResource
        try:
            builder = Gtk.Builder.new_from_resource(
                "/cloud/ivanbotty/Wizard/ui/wizard-window.ui"
            )
            
            # Get the window from the builder
            window = builder.get_object("WizardWindow")
            
            # Copy properties from the loaded window to self
            if window:
                self.set_default_size(640, 480)
                self.set_title(window.get_title() or "Launcher Setup Wizard")
                
                # Get references to important widgets
                self.carousel = self._find_carousel(window)
                self.indicator = self._find_indicator(window)
                
                # Set the content from the loaded window
                content = window.get_content()
                if content:
                    window.set_content(None)  # Remove from old window
                    self.set_content(content)
                    
                logger.info("Wizard window loaded from Blueprint UI")
            else:
                logger.error("Failed to load WizardWindow from Blueprint")
                self._create_fallback_ui()
                
        except Exception as e:
            logger.error(f"Error loading Blueprint UI: {e}")
            self._create_fallback_ui()
    
    def _find_carousel(self, widget):
        """Recursively find the Adw.Carousel widget."""
        if isinstance(widget, Adw.Carousel):
            return widget
        
        # Check if widget is a container
        if hasattr(widget, 'get_first_child'):
            child = widget.get_first_child()
            while child:
                result = self._find_carousel(child)
                if result:
                    return result
                child = child.get_next_sibling()
        
        return None
    
    def _find_indicator(self, widget):
        """Recursively find the Adw.CarouselIndicatorDots widget."""
        if isinstance(widget, Adw.CarouselIndicatorDots):
            return widget
        
        # Check if widget is a container
        if hasattr(widget, 'get_first_child'):
            child = widget.get_first_child()
            while child:
                result = self._find_indicator(child)
                if result:
                    return result
                child = child.get_next_sibling()
        
        return None
    
    def _create_fallback_ui(self):
        """Create a simple fallback UI if Blueprint loading fails."""
        logger.warning("Using fallback UI (Blueprint not available)")
        
        toolbar_view = Adw.ToolbarView()
        
        # Header bar
        header = Adw.HeaderBar()
        window_title = Adw.WindowTitle(title="Setup Wizard")
        header.set_title_widget(window_title)
        toolbar_view.add_top_bar(header)
        
        # Content box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        # Carousel
        self.carousel = Adw.Carousel()
        self.carousel.set_vexpand(True)
        self.carousel.set_hexpand(True)
        content_box.append(self.carousel)
        
        # Indicator
        self.indicator = Adw.CarouselIndicatorDots(carousel=self.carousel)
        self.indicator.set_margin_top(12)
        self.indicator.set_margin_bottom(12)
        content_box.append(self.indicator)
        
        toolbar_view.set_content(content_box)
        self.set_content(toolbar_view)
        self.set_default_size(640, 480)


class WizardPageBlueprint(Adw.Clamp):
    """
    A wizard page loaded from Blueprint UI.
    
    This class can load wizard-page.ui and allows setting
    the title, subtitle, and button text/callback dynamically.
    """
    
    def __init__(self, title="", subtitle="", button_text="Next", callback=None):
        super().__init__()
        
        self.callback = callback
        
        # Try to load from Blueprint
        try:
            builder = Gtk.Builder.new_from_resource(
                "/cloud/ivanbotty/Wizard/ui/wizard-page.ui"
            )
            
            page = builder.get_object("WizardPage")
            
            if page:
                # Get widget references
                page_title = builder.get_object("page_title")
                page_subtitle = builder.get_object("page_subtitle")
                action_button = builder.get_object("action_button")
                
                # Set properties
                if page_title:
                    page_title.set_markup(f'<span size="xx-large" weight="bold">{title}</span>')
                
                if page_subtitle:
                    page_subtitle.set_text(subtitle)
                
                if action_button:
                    action_button.set_label(button_text)
                    if callback:
                        action_button.connect("clicked", lambda *_: callback())
                
                # Copy content from loaded page
                content = page.get_child()
                if content:
                    page.set_child(None)
                    self.set_child(content)
                    self.set_maximum_size(640)
                    
                logger.info(f"Wizard page loaded from Blueprint: {title}")
            else:
                self._create_fallback_page(title, subtitle, button_text, callback)
                
        except Exception as e:
            logger.error(f"Error loading wizard page from Blueprint: {e}")
            self._create_fallback_page(title, subtitle, button_text, callback)
    
    def _create_fallback_page(self, title, subtitle, button_text, callback):
        """Create a fallback page if Blueprint loading fails."""
        self.set_maximum_size(640)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        vbox.set_margin_top(48)
        vbox.set_margin_bottom(48)
        vbox.set_margin_start(32)
        vbox.set_margin_end(32)
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)
        vbox.set_hexpand(True)
        vbox.set_vexpand(True)
        
        # Title label
        title_label = Gtk.Label()
        title_label.set_markup(f'<span size="xx-large" weight="bold">{title}</span>')
        title_label.set_wrap(True)
        title_label.set_max_width_chars(60)
        title_label.set_justify(Gtk.Justification.CENTER)
        title_label.set_halign(Gtk.Align.CENTER)
        vbox.append(title_label)
        
        # Subtitle label
        subtitle_label = Gtk.Label(label=subtitle)
        subtitle_label.add_css_class("dim-label")
        subtitle_label.set_wrap(True)
        subtitle_label.set_max_width_chars(60)
        subtitle_label.set_justify(Gtk.Justification.CENTER)
        subtitle_label.set_halign(Gtk.Align.CENTER)
        subtitle_label.set_margin_top(8)
        vbox.append(subtitle_label)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(12)
        separator.set_margin_bottom(12)
        vbox.append(separator)
        
        # Action button
        button = Gtk.Button(label=button_text)
        button.add_css_class("suggested-action")
        button.add_css_class("pill")
        button.set_halign(Gtk.Align.CENTER)
        button.set_margin_top(12)
        if callback:
            button.connect("clicked", lambda *_: callback())
        vbox.append(button)
        
        self.set_child(vbox)


def load_wizard_resources():
    """
    Load the Wizard GResource bundle.
    
    This function attempts to load the wizard resources bundle
    and register it with the GResource system.
    
    Returns:
        bool: True if resources were loaded successfully, False otherwise.
    """
    from cloud.ivanbotty.common import find_resource_file
    import os
    
    # Resource filename must match the output from meson.build
    WIZARD_RESOURCE_FILE = "wizard-resources.gresource"
    
    # Look in common locations
    search_paths = [
        os.path.join(os.path.dirname(__file__), "resources"),
        "/usr/share/launcher-app/Wizard",
        "/usr/local/share/launcher-app/Wizard",
    ]
    
    resource_path = None
    for search_path in search_paths:
        potential_path = os.path.join(search_path, WIZARD_RESOURCE_FILE)
        if os.path.exists(potential_path):
            resource_path = potential_path
            break
    
    if resource_path:
        try:
            resource = Gio.Resource.load(resource_path)
            Gio.resources_register(resource)
            logger.info(f"Wizard resources loaded from: {resource_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load Wizard resources: {e}")
            return False
    else:
        logger.warning(f"Wizard resource file not found: {WIZARD_RESOURCE_FILE}")
        return False
