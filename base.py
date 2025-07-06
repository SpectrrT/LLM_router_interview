from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, api_key: str):
        """
        Initialize the provider with API key.
        
        Args:
            api_key: The API key for the provider
        """
        self.api_key = api_key
    
    @abstractmethod
    def chat(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Send a chat completion request to the provider.
        
        Args:
            model: The model to use for completion
            messages: List of message dictionaries with 'role' and 'content' keys
            **kwargs: Additional parameters like max_tokens, temperature, top_p, etc.
            
        Returns:
            Dictionary containing the response from the provider
        """
        pass
    
    def _validate_messages(self, messages: List[Dict[str, str]]) -> None:
        """
        Validate that messages have the correct format.
        
        Args:
            messages: List of message dictionaries
            
        Raises:
            ValueError: If messages format is invalid
        """
        if not messages:
            raise ValueError("Messages list cannot be empty")
        
        for i, message in enumerate(messages):
            if not isinstance(message, dict):
                raise ValueError(f"Message {i} must be a dictionary")
            
            if 'role' not in message or 'content' not in message:
                raise ValueError(f"Message {i} must contain 'role' and 'content' keys")
            
            if not isinstance(message['role'], str) or not isinstance(message['content'], str):
                raise ValueError(f"Message {i} 'role' and 'content' must be strings")
