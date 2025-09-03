from cloud.ivanbotty.Launcher.config.config import SYSTEM_PROMPT

class AIService:
    """
    Service for handling user prompts and questions.
    """

    def __init__(self):
        # The constructor is intentionally left empty because no initialization is required for AIService at this time.
        pass

    def ask(self, question):
        """
        Ask a question to the user.

        Args:
            question (str): The question to ask.

        Returns:
            str: The user's response.
        """
        ask = SYSTEM_PROMPT + question

        return input(ask)

    def respond(self, response):
        """
        Handle the response from the user.

        Args:
            response (str): The user's response.

        Returns:
            dict: The structured response.
        """
        return {"response": response}