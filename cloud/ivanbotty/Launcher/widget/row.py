import gi
import re
import json

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Gio, Adw
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES, CATEGORY_TAG_STYLES

# Pre-compile regex patterns for better performance
_CODE_BLOCK_PATTERN = re.compile(r"(^```(?:json)?$|^```$)", re.MULTILINE)
_CODE_KEYWORDS_PATTERN = re.compile(r"\b(const|def|class|function)\b")


class Row(Gtk.ListBoxRow):
    """Enhanced row widget using native Adwaita styling.
    
    Features:
    - Configurable icon sizes
    - Native Adwaita category tags
    - Improved text hierarchy
    - Responsive layout
    """
    
    def __init__(self, app):
        super().__init__()

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

        # Type tag with native Adwaita styling
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
        """Create icon widget with configurable size from settings."""
        icon_name = icon_name or "application-x-addon-symbolic"
        icon_size = UI_CONFS[PREFERENCES].get("icon_size", 32)
        
        # Use FileIcon for absolute paths, otherwise ThemedIcon
        gicon = (
            Gio.FileIcon.new(Gio.File.new_for_path(icon_name))
            if icon_name.startswith("/")
            else Gio.ThemedIcon.new(icon_name)
        )
        
        image = Gtk.Image.new_from_gicon(gicon)
        image.set_pixel_size(icon_size)

        # Container for icon with proper spacing
        box_icon_bin = Gtk.Box()
        box_icon_bin.set_margin_top(4)
        box_icon_bin.set_margin_bottom(4)
        box_icon_bin.set_margin_start(4)
        box_icon_bin.set_margin_end(8)
        box_icon_bin.set_valign(Gtk.Align.CENTER)
        box_icon_bin.set_halign(Gtk.Align.START)
        box_icon_bin.set_size_request(icon_size + 8, icon_size + 8)
        box_icon_bin.append(image)
        
        return box_icon_bin

    def _create_name_desc_box(self, app):
        """Create the name and description layout with proper hierarchy."""
        name_desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        name_desc_box.set_valign(Gtk.Align.CENTER)

        # Name label
        name_label = Gtk.Label(label=getattr(app, "name", ""))
        name_label.set_xalign(0)
        name_label.set_hexpand(True)
        name_label.set_margin_start(0)
        name_label.set_margin_bottom(2)
        name_label.set_ellipsize(True)
        name_label.set_max_width_chars(28)
        name_label.set_halign(Gtk.Align.FILL)
        name_label.set_valign(Gtk.Align.CENTER)
        # Use heading class for better hierarchy
        name_label.add_css_class("heading")
        name_desc_box.append(name_label)

        # Description
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
            # Use dim-label for secondary text
            desc_label.add_css_class("dim-label")

            # Monospace font if code detected
            if _CODE_KEYWORDS_PATTERN.search(desc):
                desc_label.add_css_class("monospace")

            name_desc_box.set_vexpand(True)
            name_desc_box.append(desc_label)

        return name_desc_box

    def _create_tag_button(self, tag):
        """Create a category tag button using native Adwaita styles."""
        tag_button = Gtk.Button(label=tag)
        tag_button.set_valign(Gtk.Align.CENTER)
        tag_button.set_halign(Gtk.Align.END)
        tag_button.set_margin_end(8)
        tag_button.set_focusable(False)
        
        # Use native Adwaita pill style
        tag_button.add_css_class("pill")
        
        # Map tag type to Adwaita style class from configuration
        tag_lower = tag.lower()
        style_class = "accent"  # Default
        
        for tag_type, adw_class in CATEGORY_TAG_STYLES.items():
            if tag_type in tag_lower:
                style_class = adw_class
                break
        
        tag_button.add_css_class(style_class)
        
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
