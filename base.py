from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseProvider(ABC):
    """
    Abstract base class for LLM providers.
    Enforces a consistent interface and robust validation for all providers.
    """

    def __init__(self, api_key: Optional[str] = None, **config):
        """
        Initialize the provider with API key and optional config.
        Args:
            api_key: The API key for the provider (optional for some providers)
            **config: Additional provider-specific configuration
        """
        self.api_key = api_key
        self.config = config or {}

    @abstractmethod
    def chat(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Send a chat completion request to the provider.
        Args:
            model: The model to use for completion
            messages: List of message dicts with 'role' and 'content' keys
            **kwargs: Additional parameters (e.g., max_tokens, temperature, top_p, etc.)
        Returns:
            Dictionary containing the response from the provider
        """
        raise NotImplementedError("chat() must be implemented by subclasses.")

    @classmethod
    def validate_model_name(cls, model: str) -> None:
        """
        Optionally override to validate model names for a provider.
        Args:
            model: The model name to validate
        Raises:
            ValueError: If the model name is invalid
        """
        if not isinstance(model, str) or not model:
            raise ValueError("Model name must be a non-empty string.")

    @staticmethod
    def _validate_messages(messages: List[Dict[str, str]]) -> None:
        """
        Validate that messages have the correct format and content.
        Args:
            messages: List of message dictionaries
        Raises:
            ValueError: If messages format is invalid
        """
        if not isinstance(messages, list) or not messages:
            raise ValueError("Messages must be a non-empty list of dictionaries.")
        for i, message in enumerate(messages):
            if not isinstance(message, dict):
                raise ValueError(f"Message {i} must be a dictionary.")
            if set(message.keys()) != {"role", "content"}:
                raise ValueError(f"Message {i} must contain only 'role' and 'content' keys.")
            if not all(isinstance(message[k], str) and message[k].strip() for k in ("role", "content")):
                raise ValueError(f"Message {i} 'role' and 'content' must be non-empty strings.")

    @staticmethod
    def _validate_common_params(params: Dict[str, Any], allowed: Optional[set] = None) -> None:
        """
        Validate that only allowed parameters are passed to the provider.
        Args:
            params: Dictionary of parameters
            allowed: Set of allowed parameter names
        Raises:
            ValueError: If an unknown parameter is found
        """
        if allowed is not None:
            for key in params:
                if key not in allowed:
                    raise ValueError(f"Unknown parameter: {key}")
