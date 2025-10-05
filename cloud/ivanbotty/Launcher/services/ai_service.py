from google import genai
from cloud.ivanbotty.Launcher.config.config import SYSTEM_PROMPT
import cloud.ivanbotty.database.sqlite3 as db

class AIService:
    """
    Service for handling user prompts and questions.
    """

    def __init__(self):
        print("[AIService] Initializing service...")
        try:
            api_key = db.get_api_key("gemini")
            print(f"[AIService] API key retrieved: {'***' if api_key else 'None'}")
            if not api_key:
                raise ValueError("Gemini API key not found in database.")
            self.client = genai.Client(api_key=api_key)
            print("[AIService] genai.Client successfully initialized.")
        except Exception as e:
            print(f"[AIService] Initialization error: {e}")
            raise

    def ask(self, question: str) -> dict:
        """
        Ask a question to the AI model.

        Args:
            question (str): The question to ask.

        Returns:
            dict: The AI's response.
        """
        prompt = f"{SYSTEM_PROMPT}{question}"
        print(f"[AIService] Sending prompt to model: {prompt!r}")
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        print(f"[AIService] Received raw response: {response!r}")
        return self._format_response(response)

    def _format_response(self, response) -> dict:
        """
        Format the AI model's response.

        Args:
            response: The raw response from the AI model.

        Returns:
            dict: The structured response.
        """
        text = getattr(response, "text", str(response))
        print(f"[AIService] Formatted response: {text!r}")
        return {"response": text}