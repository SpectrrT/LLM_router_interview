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
    
    def chat(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Send a chat completion request to Anthropic.
        
        Args:
            model: The Anthropic model to use (e.g., 'claude-3-sonnet-20240229', 'claude-3-opus-20240229')
            messages: List of message dictionaries with 'role' and 'content' keys
            **kwargs: Additional parameters like max_tokens, temperature, top_p, etc.
            
        Returns:
            Dictionary containing the Anthropic response
        """
        self._validate_messages(messages)
        
        try:
            # Convert OpenAI-style messages to Anthropic format
            anthropic_messages = self._convert_messages(messages)
            
            response = self.client.messages.create(
                model=model,
                messages=anthropic_messages,
                **kwargs
            )
            
            return {
                'provider': 'anthropic',
                'model': model,
                'content': response.content[0].text,
                'usage': {
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens
                },
                'raw_response': response
            }
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def _convert_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Convert OpenAI-style messages to Anthropic format.
        
        Args:
            messages: List of OpenAI-style message dictionaries
            
        Returns:
            List of Anthropic-style message dictionaries
        """
        converted_messages = []
        
        for message in messages:
            role = message['role']
            content = message['content']
            
            # Map OpenAI roles to Anthropic roles
            if role == 'user':
                converted_messages.append({'role': 'user', 'content': content})
            elif role == 'assistant':
                converted_messages.append({'role': 'assistant', 'content': content})
            elif role == 'system':
                # Anthropic doesn't have system messages, so we'll prepend to the first user message
                if converted_messages and converted_messages[0]['role'] == 'user':
                    converted_messages[0]['content'] = f"{content}\n\n{converted_messages[0]['content']}"
                else:
                    # If no user message yet, create one with system content
                    converted_messages.append({'role': 'user', 'content': content})
        
        return converted_messages
