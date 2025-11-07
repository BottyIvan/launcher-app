import gi
import re
import json

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Gio, Adw
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES

# Pre-compile regex patterns for better performance
_CODE_BLOCK_PATTERN = re.compile(r"(^```(?:json)?$|^```$)", re.MULTILINE)
_CODE_KEYWORDS_PATTERN = re.compile(r"\b(const|def|class|function)\b")


class Row(Gtk.ListBoxRow):
    """Enhanced row widget with modern styling and animations.
    
    Features:
    - Smooth hover and selection animations
    - Better icon presentation with shadows
    - Improved text hierarchy and readability
    - Category tags with color coding
    - Responsive layout
    """
    
    def __init__(self, app):
        super().__init__()
        
        # Add animation class
        self.add_css_class("result-row")

        # Main row container
        row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self._apply_margins(row_box)
        row_box.set_valign(Gtk.Align.CENTER)

        # Icon
        icon_widget = self._create_icon_widget(getattr(app, "icon", None))
        row_box.append(icon_widget)

        # App name and description
        name_desc_box = self._create_name_desc_box(app)
        row_box.append(name_desc_box)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        row_box.append(spacer)

        # Type tag with category-specific styling
        tag = getattr(app, "type", "")
        if tag:
            tag_button = self._create_tag_button(tag)
            row_box.append(tag_button)

        self.set_child(row_box)

        # Adwaita style (automatic theme)
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)

    def _apply_margins(self, widget):
        """Apply consistent margins from configuration."""
        widget.set_margin_top(UI_CONFS[PREFERENCES]["margin_top"])
        widget.set_margin_bottom(UI_CONFS[PREFERENCES]["margin_bottom"])
        widget.set_margin_start(UI_CONFS[PREFERENCES]["margin_start"])
        widget.set_margin_end(UI_CONFS[PREFERENCES]["margin_end"])

    def _create_icon_widget(self, icon_name):
        """Create icon widget with modern styling and shadow."""
        icon_name = icon_name or "application-x-addon-symbolic"
        
        # Use FileIcon for absolute paths, otherwise ThemedIcon
        gicon = (
            Gio.FileIcon.new(Gio.File.new_for_path(icon_name))
            if icon_name.startswith("/")
            else Gio.ThemedIcon.new(icon_name)
        )
        
        image = Gtk.Image.new_from_gicon(gicon)
        image.set_pixel_size(32)  # Slightly larger for better visibility
        image.add_css_class("app-icon")

        # Container for icon with better spacing
        box_icon_bin = Gtk.Box()
        box_icon_bin.set_margin_top(4)
        box_icon_bin.set_margin_bottom(4)
        box_icon_bin.set_margin_start(4)
        box_icon_bin.set_margin_end(8)
        box_icon_bin.set_valign(Gtk.Align.CENTER)
        box_icon_bin.set_halign(Gtk.Align.START)
        box_icon_bin.set_size_request(40, 40)
        box_icon_bin.append(image)
        
        return box_icon_bin

    def _create_name_desc_box(self, app):
        """Create the name and description layout with improved typography."""
        name_desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        name_desc_box.set_valign(Gtk.Align.CENTER)

        # Name label with enhanced styling
        name_label = Gtk.Label(label=getattr(app, "name", ""))
        name_label.set_xalign(0)
        name_label.set_hexpand(True)
        name_label.set_margin_start(0)
        name_label.set_margin_bottom(2)
        name_label.set_ellipsize(True)
        name_label.set_max_width_chars(28)  # Slightly more space
        name_label.set_halign(Gtk.Align.FILL)
        name_label.set_valign(Gtk.Align.CENTER)
        name_label.add_css_class("app-name")
        name_desc_box.append(name_label)

        # Description with improved styling
        desc = self.prettify_description(getattr(app, "description", ""))
        if desc:
            desc_label = Gtk.Label(label=desc)
            desc_label.set_xalign(0)
            desc_label.set_hexpand(True)
            desc_label.set_vexpand(True)
            desc_label.set_wrap(True)
            desc_label.set_ellipsize(False)
            desc_label.set_max_width_chars(0)
            desc_label.set_halign(Gtk.Align.FILL)
            desc_label.set_valign(Gtk.Align.FILL)
            desc_label.add_css_class("app-description")

            # Monospace font if code detected
            if _CODE_KEYWORDS_PATTERN.search(desc):
                desc_label.add_css_class("monospace")

            name_desc_box.set_vexpand(True)
            name_desc_box.append(desc_label)

        return name_desc_box

    def _create_tag_button(self, tag):
        """Create a category tag button with color-coded styling."""
        tag_button = Gtk.Button(label=tag)
        tag_button.set_valign(Gtk.Align.CENTER)
        tag_button.set_halign(Gtk.Align.END)
        tag_button.set_margin_end(8)
        tag_button.add_css_class("category-tag")
        tag_button.add_css_class("pill")
        tag_button.set_focusable(False)
        
        # Add type-specific CSS class for color coding
        tag_lower = tag.lower()
        if "app" in tag_lower or "application" in tag_lower:
            tag_button.add_css_class("app")
        elif "math" in tag_lower or "calc" in tag_lower:
            tag_button.add_css_class("math")
        elif "ai" in tag_lower or "assistant" in tag_lower:
            tag_button.add_css_class("ai")
        elif "command" in tag_lower or "cmd" in tag_lower:
            tag_button.add_css_class("command")
        elif "file" in tag_lower:
            tag_button.add_css_class("file")
        
        return tag_button

    def prettify_description(self, description: str) -> str:
        """Clean and prettify the description for the end user."""
        if not description:
            return ""

        # Remove code block markers - use pre-compiled pattern
        cleaned = _CODE_BLOCK_PATTERN.sub("", description.strip()).strip()

        # Extract "response" from JSON if present
        try:
            data = json.loads(cleaned)
            if isinstance(data, dict) and "response" in data:
                cleaned = data["response"]
        except Exception:
            pass

        # Replace escape sequences
        cleaned = cleaned.replace("\\n", "\n").replace("\\t", "\t").strip()

        return cleaned
