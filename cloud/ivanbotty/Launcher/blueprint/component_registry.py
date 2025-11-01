"""
Component Registry - Registry of reusable UI component templates.

Provides factory methods for creating standardized UI components
with consistent styling and behavior.
"""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gio
from cloud.ivanbotty.Launcher.blueprint.style_blueprint import StyleBlueprint


class ComponentRegistry:
    """
    Factory for creating standardized UI components.
    
    Provides methods to create common UI elements with consistent
    styling, reducing code duplication and improving maintainability.
    """
    
    def __init__(self, style_blueprint=None):
        """
        Initialize component registry.
        
        Args:
            style_blueprint: StyleBlueprint instance, creates new if None
        """
        self.style = style_blueprint or StyleBlueprint()
    
    def create_button(self, label=None, icon_name=None, tooltip=None, 
                     css_classes=None, on_click=None):
        """
        Create a standardized button.
        
        Args:
            label: Button label text
            icon_name: Icon name for button
            tooltip: Tooltip text
            css_classes: List of CSS classes to apply
            on_click: Callback function for click event
            
        Returns:
            Gtk.Button: Configured button widget
        """
        button = Gtk.Button()
        
        if icon_name and label:
            # Button with icon and label
            content = Adw.ButtonContent(icon_name=icon_name, label=label)
            button.set_child(content)
        elif icon_name:
            # Icon-only button
            content = Adw.ButtonContent(icon_name=icon_name)
            button.set_child(content)
        elif label:
            # Text-only button
            button.set_label(label)
        
        if tooltip:
            button.set_tooltip_text(tooltip)
        
        if css_classes:
            self.style.apply_css_classes(button, css_classes)
        
        button.set_focus_on_click(False)
        
        if on_click:
            button.connect("clicked", on_click)
        
        return button
    
    def create_icon_button(self, icon_name, tooltip=None, css_classes=None, on_click=None):
        """
        Create an icon-only button.
        
        Args:
            icon_name: Icon name
            tooltip: Tooltip text
            css_classes: List of CSS classes
            on_click: Click callback
            
        Returns:
            Gtk.Button: Icon button widget
        """
        if css_classes is None:
            css_classes = ["flat"]
        return self.create_button(
            icon_name=icon_name,
            tooltip=tooltip,
            css_classes=css_classes,
            on_click=on_click
        )
    
    def create_label(self, text, bold=False, dim=False, align_start=False,
                    css_classes=None, max_width_chars=None, wrap=True):
        """
        Create a standardized label.
        
        Args:
            text: Label text
            bold: Whether to make text bold
            dim: Whether to dim text
            align_start: Whether to align text to start
            css_classes: List of CSS classes
            max_width_chars: Maximum width in characters
            wrap: Whether to wrap text
            
        Returns:
            Gtk.Label: Configured label widget
        """
        label = Gtk.Label(label=text)
        
        if align_start:
            label.set_xalign(0)
        
        if wrap:
            label.set_wrap(True)
        
        if max_width_chars:
            label.set_max_width_chars(max_width_chars)
        
        classes = []
        if bold:
            classes.append("bold")
        if dim:
            classes.append("dim-label")
        if css_classes:
            classes.extend(css_classes if isinstance(css_classes, list) else [css_classes])
        
        if classes:
            self.style.apply_css_classes(label, classes)
        
        return label
    
    def create_box(self, orientation=Gtk.Orientation.VERTICAL, spacing="md",
                  expand=False, margins=None):
        """
        Create a standardized box container.
        
        Args:
            orientation: Box orientation (VERTICAL or HORIZONTAL)
            spacing: Spacing preset name
            expand: Whether box should expand
            margins: Dict with margin values or None
            
        Returns:
            Gtk.Box: Configured box widget
        """
        box = Gtk.Box(orientation=orientation)
        self.style.apply_spacing(box, spacing)
        
        if expand:
            box.set_vexpand(True)
            box.set_hexpand(True)
        
        if margins:
            self.style.apply_margins(box, margins)
        
        return box
    
    def create_icon(self, icon_name, size="md", css_classes=None):
        """
        Create a standardized icon widget.
        
        Args:
            icon_name: Icon name from theme
            size: Size preset (xs, sm, md, lg, xl)
            css_classes: List of CSS classes
            
        Returns:
            Gtk.Image: Configured icon widget
        """
        gicon = Gio.ThemedIcon.new(icon_name)
        image = Gtk.Image.new_from_gicon(gicon)
        image.set_pixel_size(self.style.get_icon_size(size))
        
        if css_classes:
            self.style.apply_css_classes(image, css_classes)
        
        return image
    
    def create_scrolled_window(self, child=None, expand=True):
        """
        Create a standardized scrolled window.
        
        Args:
            child: Child widget to add
            expand: Whether to expand
            
        Returns:
            Gtk.ScrolledWindow: Configured scrolled window
        """
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        if expand:
            scrolled.set_vexpand(True)
            scrolled.set_hexpand(True)
        
        if child:
            scrolled.set_child(child)
        
        return scrolled
    
    def create_entry(self, placeholder="", width=None, height=None,
                    icon_primary=None, icon_secondary=None, css_classes=None):
        """
        Create a standardized entry widget.
        
        Args:
            placeholder: Placeholder text
            width: Entry width or None for default
            height: Entry height or None for default
            icon_primary: Primary icon name
            icon_secondary: Secondary icon name
            css_classes: List of CSS classes
            
        Returns:
            Gtk.Entry: Configured entry widget
        """
        layout = self.style.get_layout()
        entry = Gtk.Entry()
        entry.set_placeholder_text(placeholder)
        
        if width is None:
            width = layout['entry_width']
        if height is None:
            height = layout['entry_height']
        
        entry.set_size_request(width, height)
        entry.set_hexpand(True)
        
        if icon_primary:
            entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, icon_primary)
        if icon_secondary:
            entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, icon_secondary)
        
        if css_classes:
            self.style.apply_css_classes(entry, css_classes)
        
        return entry
    
    def create_list_box(self, selection_mode=Gtk.SelectionMode.SINGLE,
                       css_classes=None, expand=True):
        """
        Create a standardized list box.
        
        Args:
            selection_mode: Selection mode
            css_classes: List of CSS classes
            expand: Whether to expand
            
        Returns:
            Gtk.ListBox: Configured list box widget
        """
        list_box = Gtk.ListBox()
        list_box.set_selection_mode(selection_mode)
        
        if expand:
            list_box.set_vexpand(True)
            list_box.set_hexpand(True)
        
        if css_classes:
            self.style.apply_css_classes(list_box, css_classes)
        
        return list_box
    
    def create_tag_button(self, label, css_classes=None):
        """
        Create a styled tag button (non-interactive badge).
        
        Args:
            label: Tag text
            css_classes: Additional CSS classes
            
        Returns:
            Gtk.Button: Tag button widget
        """
        button = Gtk.Button(label=label)
        button.set_valign(Gtk.Align.CENTER)
        button.set_halign(Gtk.Align.END)
        button.set_focusable(False)
        
        default_classes = ["round", "raised", "accent", "monospace"]
        if css_classes:
            default_classes.extend(css_classes if isinstance(css_classes, list) else [css_classes])
        
        self.style.apply_css_classes(button, default_classes)
        
        return button
