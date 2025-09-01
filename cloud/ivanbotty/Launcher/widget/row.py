import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Gio, Adw
from cloud.ivanbotty.Launcher.config.config import UI_CONFS, PREFERENCES

class Row(Gtk.ListBoxRow):
    def __init__(self, app):
        super().__init__()

        # Main row container
        row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row_box.set_margin_top(UI_CONFS[PREFERENCES]["margin_top"])
        row_box.set_margin_bottom(UI_CONFS[PREFERENCES]["margin_bottom"])
        row_box.set_margin_start(UI_CONFS[PREFERENCES]["margin_start"])
        row_box.set_margin_end(UI_CONFS[PREFERENCES]["margin_end"])
        row_box.set_valign(Gtk.Align.CENTER)

        # Icon
        icon_name = getattr(app, "icon", None)
        if icon_name:
            icon_widget = self.create_icon_image(icon_name)
            icon_widget.set_pixel_size(32)
        else:
            icon_widget = Gtk.Image.new_from_icon_name("application-x-addon-symbolic")
            icon_widget.set_pixel_size(32)

        box_icon_bin = Gtk.Box()
        box_icon_bin.set_margin_top(4)
        box_icon_bin.set_margin_bottom(4)
        box_icon_bin.set_margin_start(4)
        box_icon_bin.set_margin_end(12)
        box_icon_bin.set_size_request(40, 40)
        box_icon_bin.set_valign(Gtk.Align.CENTER)
        box_icon_bin.set_halign(Gtk.Align.START)
        box_icon_bin.append(icon_widget)

        row_box.append(box_icon_bin)

        # App name and description (vertical box)
        name_desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        name_desc_box.set_valign(Gtk.Align.CENTER)

        name_label = Gtk.Label(label=getattr(app, "name", ""))
        name_label.set_xalign(0)
        name_label.set_hexpand(True)
        name_label.set_margin_start(0)
        name_label.set_margin_bottom(2)
        name_label.set_ellipsize(True)
        name_label.set_max_width_chars(24)
        name_label.set_halign(Gtk.Align.FILL)
        name_label.set_valign(Gtk.Align.CENTER)

        desc = getattr(app, "description", "")
        if desc:
            desc_label = Gtk.Label(label=desc)
            desc_label.set_xalign(0)
            desc_label.set_hexpand(True)
            desc_label.set_ellipsize(True)
            desc_label.set_max_width_chars(32)
            desc_label.set_halign(Gtk.Align.FILL)
            desc_label.set_valign(Gtk.Align.CENTER)
            name_desc_box.append(name_label)
            name_desc_box.append(desc_label)
        else:
            name_desc_box.append(name_label)

        row_box.append(name_desc_box)

        # Spacer
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        row_box.append(spacer)

        # Type tag (styled)
        tag = getattr(app, "type", "")
        if tag:
            tag_label = Gtk.Label(label=tag)
            tag_label.set_xalign(1)
            tag_label.set_margin_end(8)
            tag_label.set_ellipsize(True)
            tag_label.set_max_width_chars(12)
            row_box.append(tag_label)

        self.set_child(row_box)

        # Add Adw style for row highlight
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.PREFER_LIGHT)

    def create_icon_image(self, icon_name):
        gicon = Gio.ThemedIcon.new(icon_name)
        image = Gtk.Image.new_from_gicon(gicon)
        return image