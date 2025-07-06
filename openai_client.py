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
        self._validate_messages(messages)
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            
            return {
                'provider': 'openai',
                'model': model,
                'content': response.choices[0].message.content,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                },
                'raw_response': response
            }
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
