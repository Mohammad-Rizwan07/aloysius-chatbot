"""
Google Gemini API integration for LLM calls.
Handles all interactions with Google's Gemini models.
"""

import logging
from typing import Optional
import google.generativeai as genai
from config.config import config

logger = logging.getLogger(__name__)


class GeminiLLM:
    """
    Wrapper for Google Gemini API interactions.
    Handles model initialization, API calls, and error handling.
    """

    def __init__(self):
        """Initialize Gemini API client"""
        try:
            genai.configure(api_key=config.gemini.api_key)
            self.model = genai.GenerativeModel(config.gemini.model)
            logger.info(f"Gemini API initialized with model: {config.gemini.model}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {e}")
            raise

    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_instruction: Optional[str] = None,
    ) -> str:
        """
        Generate text using Gemini API.
        """

        try:
            temperature = temperature if temperature is not None else config.gemini.temperature
            max_tokens = max_tokens if max_tokens is not None else config.gemini.max_tokens

            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )

            # Create model WITH system instruction if provided
            if system_instruction:
                model = genai.GenerativeModel(
                    model_name=config.gemini.model,
                    system_instruction=system_instruction,
                    generation_config=generation_config,
                )
            else:
                model = self.model
                model.generation_config = generation_config

            # IMPORTANT: pass generation_config here to preserve formatting
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )

            logger.debug("Gemini API call successful")
            return response.text.strip()

        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            raise

    def generate_with_context(
        self,
        query: str,
        context: list[str],
        system_instruction: str,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Generate response using RAG context.
        """

        try:
            # Format context clearly (important for Gemini reasoning)
            context_text = "\n\n".join(
                [f"[Context {i+1}]\n{chunk}" for i, chunk in enumerate(context)]
            )

            prompt = f"""
RELEVANT INFORMATION:
{context_text}

USER QUESTION:
{query}

ANSWER:
""".strip()

            return self.generate(
                prompt=prompt,
                system_instruction=system_instruction,
                temperature=temperature,
            )

        except Exception as e:
            logger.error(f"Error generating response with context: {e}")
            raise

    def health_check(self) -> bool:
        """Check if Gemini API is accessible."""
        try:
            response = self.model.generate_content("test")
            logger.info("Gemini API health check passed")
            return bool(response.text)
        except Exception as e:
            logger.error(f"Gemini API health check failed: {e}")
            return False


# Singleton instance
_llm_instance: Optional[GeminiLLM] = None


def get_llm() -> GeminiLLM:
    """Get or create the global Gemini LLM instance."""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = GeminiLLM()
    return _llm_instance
