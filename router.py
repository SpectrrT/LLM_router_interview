from typing import Dict, Any, List
from base import BaseProvider
from openai_client import OpenAIProvider
from anthropic_client import AnthropicProvider


class LLMRouter:
    """Router class that dispatches chat calls to the correct provider."""
    
    def __init__(self, provider_name: str, api_key: str):
        """
        Initialize the router with a specific provider.
        
        Args:
            provider_name: Name of the provider ('openai' or 'anthropic')
            api_key: API key for the provider
        """
        self.provider_name = provider_name.lower()
        self.api_key = api_key
        self.provider = self._create_provider()
    
    def _create_provider(self) -> BaseProvider:
        """
        Create the appropriate provider instance.
        
        Returns:
            Provider instance
            
        Raises:
            ValueError: If provider name is not supported
        """
        if self.provider_name == 'openai':
            return OpenAIProvider(self.api_key)
        elif self.provider_name == 'anthropic':
            return AnthropicProvider(self.api_key)
        else:
            raise ValueError(f"Unsupported provider: {self.provider_name}. Supported providers: 'openai', 'anthropic'")
    
    def chat(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Send a chat completion request using the configured provider.
        
        Args:
            model: The model to use for completion
            messages: List of message dictionaries with 'role' and 'content' keys
            **kwargs: Additional parameters like max_tokens, temperature, top_p, etc.
            
        Returns:
            Dictionary containing the response from the provider
        """
        return self.provider.chat(model, messages, **kwargs)
    
    def get_provider_info(self) -> Dict[str, str]:
        """
        Get information about the current provider.
        
        Returns:
            Dictionary with provider information
        """
        return {
            'provider': self.provider_name,
            'class': self.provider.__class__.__name__
        }


# Convenience class that mimics OpenAI's client interface
class LLMClient:
    """Client class that provides OpenAI-like interface."""
    
    def __init__(self, provider_name: str, api_key: str):
        """
        Initialize the client.
        
        Args:
            provider_name: Name of the provider ('openai' or 'anthropic')
            api_key: API key for the provider
        """
        self.router = LLMRouter(provider_name, api_key)
    
    @property
    def chat(self):
        """Return chat completions interface."""
        return ChatCompletions(self.router)


class ChatCompletions:
    """Chat completions interface that mimics OpenAI's style."""
    
    def __init__(self, router: LLMRouter):
        """
        Initialize chat completions interface.
        
        Args:
            router: The LLM router instance
        """
        self.router = router
    
    def create(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Create a chat completion.
        
        Args:
            model: The model to use for completion
            messages: List of message dictionaries with 'role' and 'content' keys
            **kwargs: Additional parameters like max_tokens, temperature, top_p, etc.
            
        Returns:
            Dictionary containing the response from the provider
        """
        return self.router.chat(model, messages, **kwargs)
    
    @property
    def completions(self):
        """Return self to support chat.completions.create() syntax."""
        return self
