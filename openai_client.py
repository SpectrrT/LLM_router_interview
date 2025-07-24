from openai import OpenAI
from typing import List, Dict, Any
from base import BaseProvider


class OpenAIProvider(BaseProvider):
    """OpenAI provider implementation."""
    
    def __init__(self, api_key: str):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key
        """
        super().__init__(api_key)
        # Initialize the OpenAI client
        self.client = OpenAI(api_key=api_key)
    
    provider_name = "openai"

    def chat(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Send a chat completion request to OpenAI.
        Args:
            model: The OpenAI model to use (e.g., 'gpt-3.5-turbo', 'gpt-4')
            messages: List of message dictionaries with 'role' and 'content' keys
            **kwargs: Additional parameters like max_tokens, temperature, top_p, etc.
        Returns:
            Dictionary containing the OpenAI response
        """
        self.validate_model_name(model)
        self._validate_messages(messages)
        allowed_params = {
            "max_tokens", "temperature", "top_p", "n", "stream", "stop", "presence_penalty",
            "frequency_penalty", "logit_bias", "user", "response_format", "seed", "tools"
        }
        self._validate_common_params(kwargs, allowed=allowed_params)

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            return {
                'provider': self.provider_name,
                'model': model,
                'content': response.choices[0].message.content if response.choices else "",
                'usage': {
                    'prompt_tokens': getattr(response.usage, 'prompt_tokens', None),
                    'completion_tokens': getattr(response.usage, 'completion_tokens', None),
                    'total_tokens': getattr(response.usage, 'total_tokens', None)
                },
                'raw_response': response
            }
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}") from e
