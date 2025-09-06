class BaseInputHandler:
    def can_handle(self, text: str) -> bool:
        """
        Determines if this handler can process the given input text.

        Args:
            text (str): The input text to evaluate.

        Returns:
            bool: True if the handler can process the text, False otherwise.
        """
        raise NotImplementedError

    def handle(self, text: str, services: dict):
        """
        Executes the action associated with the input text.

        Args:
            text (str): The input text to handle.
            services (dict): A dictionary of available services for processing.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError
