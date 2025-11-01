import gi
import re
import json

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Gio, Adw
from cloud.ivanbotty.Launcher.blueprint import UIBlueprint


class Row(Gtk.ListBoxRow):
    def __init__(self, app):
        super().__init__()
        
        # Use blueprint for consistent styling
        self.ui_blueprint = UIBlueprint()
        layout = self.ui_blueprint.style.get_layout()

        # Main row container
        row_box = self.ui_blueprint.components.create_box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing="lg",
            expand=False
        )
        
        # Apply margins using blueprint
        self.ui_blueprint.style.apply_margins(row_box, {
            'top': layout['margin_top'],
            'bottom': layout['margin_bottom'],
            'start': layout['margin_start'],
            'end': layout['margin_end']
        })
        
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

        # Type tag
        tag = getattr(app, "type", "")
        if tag:
            tag_button = self.ui_blueprint.components.create_tag_button(tag)
            tag_button.set_margin_end(8)
            row_box.append(tag_button)

        self.set_child(row_box)

        # Adwaita style (automatic theme)
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.DEFAULT)

    def _create_icon_widget(self, icon_name):
        icon_name = icon_name or "application-x-addon-symbolic"
        image = self.ui_blueprint.components.create_icon(
            icon_name=icon_name,
            size="md",
            css_classes=["icon-dropshadow"]
        )

        box_icon_bin = Gtk.Box()
        box_icon_bin.set_margin_top(2)
        box_icon_bin.set_margin_bottom(2)
        box_icon_bin.set_margin_start(2)
        box_icon_bin.set_margin_end(8)
        box_icon_bin.set_valign(Gtk.Align.CENTER)
        box_icon_bin.set_halign(Gtk.Align.START)
        box_icon_bin.set_size_request(36, 36)
        box_icon_bin.append(image)
        return box_icon_bin

    def _create_name_desc_box(self, app):
        name_desc_box = self.ui_blueprint.components.create_box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing="xs",
            expand=False
        )
        name_desc_box.set_valign(Gtk.Align.CENTER)

        # Name label
        name_label = self.ui_blueprint.components.create_label(
            text=getattr(app, "name", ""),
            align_start=True,
            max_width_chars=24,
            wrap=False
        )
        name_label.set_hexpand(True)
        name_label.set_margin_start(0)
        name_label.set_margin_bottom(2)
        name_label.set_ellipsize(True)
        name_label.set_halign(Gtk.Align.FILL)
        name_label.set_valign(Gtk.Align.CENTER)
        name_desc_box.append(name_label)

        # Description
        desc = self.prettify_description(getattr(app, "description", ""))
        if desc:
            desc_label = self.ui_blueprint.components.create_label(
                text=desc,
                align_start=True,
                max_width_chars=0,
                wrap=True
            )
            desc_label.set_hexpand(True)
            desc_label.set_vexpand(True)
            desc_label.set_ellipsize(False)
            desc_label.set_halign(Gtk.Align.FILL)
            desc_label.set_valign(Gtk.Align.FILL)

            # Monospace font if code detected
            if re.search(r"\b(const|def|class|function)\b", desc):
                desc_label.add_css_class("monospace")

            name_desc_box.set_vexpand(True)
            name_desc_box.append(desc_label)

        return name_desc_box

    def prettify_description(self, description: str) -> str:
        """Clean and prettify the description for the end user."""
        if not description:
            return ""

        # Remove code block markers
        cleaned = re.sub(r"(^```(?:json)?$|^```$)", "", description.strip(), flags=re.MULTILINE).strip()

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
