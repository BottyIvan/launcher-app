import re
from gi.repository import Gtk
import cloud.ivanbotty.Launcher.handlers.base_input_handler as bih

class MathHandler(bih.BaseInputHandler):
    def can_handle(self, text):
        return bool(re.fullmatch(r"[0-9+\-*/(). ]+", text.strip()))

    def handle(self, text, services, view):
        result = services["math"].calculate(text)
        view.insert(Gtk.Label(label=f"Result: {result}"), 0)
