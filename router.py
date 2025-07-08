from typing import Dict, Any, List
from base import BaseProvider
from openai_client import OpenAIProvider
from anthropic_client import AnthropicProvider


class LLMRouter:
    """Router class that dispatches chat calls to the correct provider."""
    
    _PROVIDER_REGISTRY = {
        'openai': OpenAIProvider,
        'anthropic': AnthropicProvider,
    }

    def __init__(self, provider_name: str, api_key: str, **provider_config):
        """
        Initialize the router with a specific provider.
        Args:
            provider_name: Name of the provider (e.g., 'openai', 'anthropic')
            api_key: API key for the provider
            **provider_config: Additional provider-specific configuration
        """
        self.provider_name = provider_name.lower()
        self.api_key = api_key
        self.provider_config = provider_config
        self.provider = self._create_provider()

    def _create_provider(self) -> BaseProvider:
        """
        Create the appropriate provider instance from the registry.
        Returns:
            Provider instance
        Raises:
            ValueError: If provider name is not supported
        """
        provider_cls = self._PROVIDER_REGISTRY.get(self.provider_name)
        if not provider_cls:
            raise ValueError(f"Unsupported provider: {self.provider_name}. Supported providers: {list(self._PROVIDER_REGISTRY.keys())}")
        return provider_cls(self.api_key, **self.provider_config)
    
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
            'provider': getattr(self.provider, 'provider_name', self.provider_name),
            'class': self.provider.__class__.__name__,
            'config': str(self.provider_config)
        }


# Convenience class that mimics OpenAI's client interface
class LLMClient:
    """Client class that provides OpenAI-like interface."""

    def __init__(self, provider_name: str, api_key: str, **provider_config):
        """
        Initialize the client.
        Args:
            provider_name: Name of the provider (e.g., 'openai', 'anthropic')
            api_key: API key for the provider
            **provider_config: Additional provider-specific configuration
        """
        self.router = LLMRouter(provider_name, api_key, **provider_config)

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
