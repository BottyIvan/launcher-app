import re
from gi.repository import Gio
import cloud.ivanbotty.Launcher.handlers.base_input_handler as bih
from cloud.ivanbotty.Launcher.models.applications_model import ApplicationModel

class MathHandler(bih.BaseInputHandler):
    def can_handle(self, text):
        return bool(re.fullmatch(r"[0-9+\-*/(). ]+", text.strip()))

    def handle(self, text, services):
        list_model = Gio.ListStore(item_type=ApplicationModel)
        list_model.append(ApplicationModel(
            type="math",
            name=f"Result: {eval(text)}",
            description=f"Evaluated expression: {text}",
            exec_cmd=None,
            icon="accessories-calculator"
        ))
        return list_model