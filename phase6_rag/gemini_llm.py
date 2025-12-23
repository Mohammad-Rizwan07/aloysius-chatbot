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
        
        Args:
            prompt: The user prompt
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum output tokens
            system_instruction: System-level instructions for the model
            
        Returns:
            Generated text response
        """
        try:
            temperature = temperature or config.gemini.temperature
            max_tokens = max_tokens or config.gemini.max_tokens
            
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            # Create model with system instruction if provided
            if system_instruction:
                model = genai.GenerativeModel(
                    config.gemini.model,
                    system_instruction=system_instruction,
                    generation_config=generation_config,
                )
            else:
                model = self.model
                model.generation_config = generation_config
            
            response = model.generate_content(prompt)
            
            logger.debug(f"Gemini API call successful")
            return response.text
            
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
        
        Args:
            query: User query
            context: List of relevant context chunks
            system_instruction: System prompt with RAG instructions
            temperature: Sampling temperature
            
        Returns:
            Generated response with context
        """
        try:
            # Format context
            context_text = "\n\n".join([f"[Context {i+1}]\n{chunk}" 
                                       for i, chunk in enumerate(context)])
            
            # Build prompt with context
            prompt = f"""{system_instruction}

RELEVANT INFORMATION:
{context_text}

USER QUESTION:
{query}

ANSWER:"""
            
            return self.generate(
                prompt=prompt,
                temperature=temperature,
            )
            
        except Exception as e:
            logger.error(f"Error generating response with context: {e}")
            raise
    
    def health_check(self) -> bool:
        """
        Check if Gemini API is accessible.
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            response = self.model.generate_content("test")
            logger.info("Gemini API health check passed")
            return bool(response.text)
        except Exception as e:
            logger.error(f"Gemini API health check failed: {e}")
            return False


# Global LLM instance
_llm_instance: Optional[GeminiLLM] = None


def get_llm() -> GeminiLLM:
    """
    Get or create the global Gemini LLM instance.
    Follows singleton pattern for efficient resource usage.
    
    Returns:
        GeminiLLM instance
    """
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = GeminiLLM()
    return _llm_instance
