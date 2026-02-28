from core.prompt_compiler import PromptCompiler
from core.llm_service import LLMService


class IntentEngine:
    """
    Engine responsible for generating email content based on intent state.
    Coordinates between prompt compilation and LLM service.
    """

    def __init__(self):
        """Initialize the intent engine."""
        self.compiler = PromptCompiler()
        self.llm_service = LLMService()

    def generate(self, state):
        """
        Generate email content based on the provided intent state.

        Args:
            state (IntentState): The intent state object containing domain,
                                 recipient, category, scenario, and metadata

        Returns:
            str: Generated email content

        Raises:
            Exception: If email generation fails
        """
        try:
            # Compile the intent brief from the state
            brief = self.compiler.compile_intent_brief(state)

            # Generate content using LLM service
            email_content = self.llm_service.generate(brief)

            return email_content

        except Exception as e:
            raise Exception(f"Failed to generate email: {str(e)}")