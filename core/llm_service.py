import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    logger.error("✗ OPENAI_API_KEY not found in .env")
    raise RuntimeError("OPENAI_API_KEY not found in .env")

client = OpenAI(api_key=api_key)
logger.info("✓ OpenAI client initialized")


class LLMService:
    """
    Service for interacting with LLM (OpenAI).
    Keeps API logic isolated from business logic.
    """

    @staticmethod
    def generate(intent_brief: str) -> str:
        """
        Generate email content using OpenAI API.

        Args:
            intent_brief (str): The compiled prompt brief

        Returns:
            str: Generated email content
        """
        try:
            logger.info("→ Requesting email generation from OpenAI")

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an experienced professional communicator.\n"
                            "Write emails that feel written by a real person.\n"
                            "Avoid generic filler sentences.\n"
                            "Avoid textbook phrasing.\n"
                            "Make the email natural and context-aware.\n"
                            "Do not use placeholders.\n"
                        ),
                    },
                    {
                        "role": "user",
                        "content": intent_brief,
                    },
                ],
                temperature=0.9,
                max_tokens=1000,
            )

            content = response.choices[0].message.content
            logger.info("✓ Email generated successfully")
            return content

        except Exception as e:
            logger.error(f"✗ LLM generation failed: {str(e)}", exc_info=True)
            return f"LLM ERROR: {str(e)}"


def generate_email(intent_brief: str) -> str:
    """
    Wrapper function used by FastAPI.

    Args:
        intent_brief (str): The compiled prompt brief

    Returns:
        str: Generated email content
    """
    return LLMService.generate(intent_brief)