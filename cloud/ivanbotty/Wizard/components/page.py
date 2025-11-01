import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
from typing import Callable

class Page:
    @staticmethod
    def make_page(title: str, subtitle: str, button_text: str, callback: Callable) -> Adw.Clamp:
        """
        Creates a compact, Adwaita-conformant onboarding page.
        Args:
            title (str): The main title of the page.
            subtitle (str): The subtitle or description.
            button_text (str): Text for the action button.
            callback (Callable): Function to call when button is clicked.
        Returns:
            Adw.Clamp: The constructed page widget.
        """
        clamp = Adw.Clamp()  # Container that constrains the maximum width
        clamp.set_maximum_size(640)

        # Vertical box to arrange widgets
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        vbox.set_margin_top(48)
        vbox.set_margin_bottom(48)
        vbox.set_margin_start(32)
        vbox.set_margin_end(32)
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)
        vbox.set_hexpand(True)
        vbox.set_vexpand(True)

        # Title and subtitle labels
        title_label = Page._create_label(title, markup=True, size='xx-large', weight='bold')
        subtitle_label = Page._create_label(subtitle, markup=True, dim=True, margin_top=8)

        # Separator line
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(12)
        separator.set_margin_bottom(12)

        # Action button
        button = Gtk.Button(label=button_text)
        button.add_css_class("suggested-action")
        button.set_halign(Gtk.Align.CENTER)
        button.set_margin_top(12)
        button.connect("clicked", lambda *_: callback())

        # Add widgets to the vertical box
        vbox.append(title_label)
        vbox.append(subtitle_label)
        vbox.append(separator)
        vbox.append(button)

        clamp.set_child(vbox)
        return clamp

    @staticmethod
    def _create_label(
        text: str,
        markup: bool = False,
        size: str = None,
        weight: str = None,
        dim: bool = False,
        margin_top: int = 0,
        wrap: bool = True,
        max_width_chars: int = 60,
        selectable: bool = False,
    ) -> Gtk.Label:
        """
        Helper to create a Gtk.Label with improved formatting and styling.
        Args:
            text (str): The label text.
            markup (bool): Whether to use Pango markup.
            size (str): Markup size (e.g., 'xx-large').
            weight (str): Markup weight (e.g., 'bold').
            dim (bool): Whether to add a dim CSS class.
            margin_top (int): Top margin in pixels.
            wrap (bool): Enable text wrapping.
            max_width_chars (int): Maximum width in characters before wrapping.
            selectable (bool): Whether the label text is selectable.
        Returns:
            Gtk.Label: The configured label widget.
        """
        label = Gtk.Label()
        if markup:
            markup_text = text
            if size or weight:
                markup_text = "<span"
                if size:
                    markup_text += f" size='{size}'"
                if weight:
                    markup_text += f" weight='{weight}'"
                markup_text += f">{text}</span>"
            label.set_markup(markup_text)
        else:
            label.set_text(text)

        label.set_wrap(wrap)
        label.set_max_width_chars(max_width_chars)
        label.set_justify(Gtk.Justification.CENTER)
        label.set_halign(Gtk.Align.CENTER)
        label.set_valign(Gtk.Align.START)
        label.set_selectable(selectable)

        if dim:
            label.add_css_class("dim-label")
        if margin_top:
            label.set_margin_top(margin_top)
        return label
