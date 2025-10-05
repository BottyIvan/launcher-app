from google import genai
from cloud.ivanbotty.Launcher.config.config import SYSTEM_PROMPT
from cloud.ivanbotty.database.sqlite3 import db

class AIService:
    """
    Service for handling user prompts and questions.
    """

    def __init__(self):
        api_key = db.get_api_key("gemini")
        if not api_key:
            raise ValueError("Gemini API key not found in database.")
        self.client = genai.Client(api_key)

    def ask(self, question: str) -> dict:
        """
        Ask a question to the AI model.

        Args:
            question (str): The question to ask.

        Returns:
            dict: The AI's response.
        """
        prompt = f"{SYSTEM_PROMPT}{question}"
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return self._format_response(response)

    def _format_response(self, response) -> dict:
        """
        Format the AI model's response.

        Args:
            response: The raw response from the AI model.

        Returns:
            dict: The structured response.
        """
        # Assuming response has a 'text' attribute; adjust if needed
        text = getattr(response, "text", str(response))
        return {"response": text}