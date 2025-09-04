import re
from gi.repository import Gtk
import cloud.ivanbotty.Launcher.handlers.base_input_handler as bih

class MathHandler(bih.BaseInputHandler):
    def can_handle(self, text):
        return bool(re.fullmatch(r"[0-9+\-*/(). ]+", text.strip()))

    def handle(self, text, services, view):
        try:
            expression = text.strip()
            result = services["math"].calculate(expression)

            # Card container
            container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            container.set_margin_top(12)
            container.set_margin_bottom(12)
            container.set_margin_start(12)
            container.set_margin_end(12)

            # Expression row
            expr_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            label_expr = Gtk.Label(label=expression)
            label_expr.set_selectable(True)
            label_expr.set_xalign(0)  # align left
            label_expr.add_css_class("title-2")
            expr_row.append(label_expr)

            # Separator
            separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

            # Result row
            result_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            result_row.set_halign(Gtk.Align.END)  # right align result row
            label_equals = Gtk.Label(label="=")
            label_equals.add_css_class("dim-label")
            label_result = Gtk.Label(label=f"{result}")
            label_result.set_selectable(True)
            label_result.add_css_class("title-1")
            result_row.append(label_equals)
            result_row.append(label_result)

            # Build card content
            container.append(expr_row)
            container.append(separator)
            container.append(result_row)

            # Apply card style to the output view
            view.add_css_class("card")
            view.set_child(container)

        except Exception as e:
            error_label = Gtk.Label(label=f"Error: {e}")
            error_label.add_css_class("error")
            view.set_child(error_label)
