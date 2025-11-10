"""Math expression handler.

This module provides a handler for processing mathematical expressions
entered by the user in the launcher search bar.
"""

import re
from typing import Dict

from gi.repository import Gio

from cloud.ivanbotty.LightFlow.handlers.base_input_handler import BaseInputHandler
from cloud.ivanbotty.LightFlow.models.applications_model import ApplicationModel


class MathHandler(BaseInputHandler):
    """Handler for mathematical expression evaluation.

    Attributes:
        MATH_PATTERN: Regular expression pattern for valid math expressions
    """

    # Regular expression to match valid math expressions (digits, operators, parentheses, spaces)
    MATH_PATTERN = re.compile(r"^[\d+\-*/().\s]+$")

    def can_handle(self, text: str) -> bool:
        """Check if the input text is a valid mathematical expression.

        Args:
            text: Input text to evaluate

        Returns:
            True if text matches a valid math expression pattern
        """
        text = text.strip()
        return bool(text and self.MATH_PATTERN.fullmatch(text))

    def handle(self, text: str, services: Dict) -> Gio.ListStore:
        """Evaluate the mathematical expression and return results.

        Args:
            text: Mathematical expression to evaluate
            services: Dictionary of available services (must include 'math')

        Returns:
            Gio.ListStore containing the calculation result or error
        """
        # Create a new Gio.ListStore to hold the result
        list_model = Gio.ListStore(item_type=ApplicationModel)

        # Calculate the result using the provided math service
        result, error = services["math"].calculate(text)

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
        list_model.append(
            ApplicationModel(
                type="math", name=name, description=description, exec_cmd=None, icon=icon
            )
        )

        return list_model
