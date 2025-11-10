from google import genai
from cloud.ivanbotty.LightFlow.config.config import SYSTEM_PROMPT
import cloud.ivanbotty.database.sqlite3 as db
import logging

logger = logging.getLogger(__name__)


class AIService:
    """
    Service for handling user prompts and questions.
    """

    def __init__(self):
        logger.info("Initializing AIService")
        try:
            api_key = db.get_api_key("gemini")
            logger.debug(f"API key retrieved: {'***' if api_key else 'None'}")
            if not api_key:
                raise ValueError("Gemini API key not found in database.")
            self.client = genai.Client(api_key=api_key)
            logger.info("genai.Client successfully initialized")
        except Exception as e:
            logger.error(f"AIService initialization error: {e}")
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
        logger.debug(f"Sending prompt to model: prompt={prompt!r}")
        response = self.client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        logger.debug(f"Received raw response: response={response!r}")
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
        logger.debug(f"Formatted response: text={text!r}")
        return text
