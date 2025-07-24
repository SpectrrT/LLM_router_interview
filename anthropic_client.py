import anthropic
from typing import List, Dict, Any
from base import BaseProvider


class AnthropicProvider(BaseProvider):
    """Anthropic provider implementation."""
    
    def __init__(self, api_key: str):
        """
        Initialize Anthropic provider.
        
        Args:
            api_key: Anthropic API key
        """
        super().__init__(api_key)
        # Initialize the Anthropic client
        # You'll need to add your Anthropic API key here
        self.client = anthropic.Anthropic(api_key=api_key)
    
    provider_name = "anthropic"

    def chat(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Send a chat completion request to Anthropic.
        Args:
            model: The Anthropic model to use
            messages: List of message dicts with 'role' and 'content' keys
            **kwargs: Additional parameters (max_tokens, temperature, top_p, etc.)
        Returns:
            Dictionary containing the Anthropic response
        """
        self.validate_model_name(model)
        self._validate_messages(messages)
        allowed_params = {"max_tokens", "temperature", "top_p", "stop_sequences", "metadata"}
        self._validate_common_params(kwargs, allowed=allowed_params)

        try:
            anthropic_messages = self._convert_messages(messages)
            response = self.client.messages.create(
                model=model,
                messages=anthropic_messages,
                **kwargs
            )
            return {
                'provider': self.provider_name,
                'model': model,
                'content': response.content[0].text if response.content else "",
                'usage': {
                    'input_tokens': getattr(response.usage, 'input_tokens', None),
                    'output_tokens': getattr(response.usage, 'output_tokens', None)
                },
                'raw_response': response
            }
        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {str(e)}") from e
    
    def _convert_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Convert OpenAI-style messages to Anthropic format.
        - System messages are prepended to the first user message, or become a user message if none exists.
        Args:
            messages: List of OpenAI-style message dictionaries
        Returns:
            List of Anthropic-style message dictionaries
        """
        converted = []
        system_content = []
        for message in messages:
            role = message['role']
            content = message['content']
            if role == 'system':
                system_content.append(content)
            elif role in ('user', 'assistant'):
                converted.append({'role': role, 'content': content})

        if system_content:
            system_text = "\n\n".join(system_content)
            if converted and converted[0]['role'] == 'user':
                converted[0]['content'] = f"{system_text}\n\n{converted[0]['content']}"
            else:
                converted.insert(0, {'role': 'user', 'content': system_text})

        return converted
