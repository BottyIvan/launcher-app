import re
from gi.repository import Gio
from cloud.ivanbotty.Launcher.handlers.base_input_handler import BaseInputHandler
from cloud.ivanbotty.Launcher.models.applications_model import ApplicationModel

class MathHandler(BaseInputHandler):
    # Regular expression to match valid math expressions (digits, operators, parentheses, spaces)
    MATH_PATTERN = re.compile(r"^[\d+\-*/().\s]+$")

    def can_handle(self, text):
        # Check if the input text is a valid math expression
        text = text.strip()
        return bool(text) and self.MATH_PATTERN.fullmatch(text)

    def handle(self, text, services):
        # Create a new Gio.ListStore to hold the result
        list_model = Gio.ListStore(item_type=ApplicationModel)
        # Calculate the result using the provided math service
        result, error = services['math'].calculate(text)
        if error:
            # If there is an error, show an error message
            name = "Error"
            description = error
            icon = "dialog-error"
        else:
            # If calculation is successful, show the result
            name = f"Result: {result}"
            description = f"{text} = {result}"
            icon = "accessories-calculator"
        # Append the result or error to the list model
        list_model.append(ApplicationModel(
            type="math",
            name=name,
            description=description,
            exec_cmd=None,
            icon=icon
        ))
        return list_model