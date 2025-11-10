"""Base input handler interface.

This module defines the base interface that all input handlers must implement
to process user input in the launcher.
"""

from typing import Dict


class BaseInputHandler:
    """Base class for input handlers.

    All input handlers should inherit from this class and implement
    the can_handle and handle methods.
    """

    def can_handle(self, text: str) -> bool:
        """Determine if this handler can process the given input text.

        Args:
            text: The input text to evaluate

        Returns:
            True if the handler can process the text, False otherwise

        Raises:
            NotImplementedError: If not implemented in subclass
        """
        raise NotImplementedError("Subclasses must implement can_handle()")

    def handle(self, text: str, services: Dict):
        """Execute the action associated with the input text.

        Args:
            text: The input text to handle
            services: A dictionary of available services for processing

        Returns:
            A Gio.ListStore containing results to display

        Raises:
            NotImplementedError: If not implemented in subclass
        """
        raise NotImplementedError("Subclasses must implement handle()")
