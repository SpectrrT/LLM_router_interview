"""
LLM Router - A unified interface for multiple LLM providers.

This package provides a modular and scalable interface to multiple LLM providers,
starting with OpenAI and Anthropic.
"""

from base import BaseProvider
from openai_client import OpenAIProvider
from anthropic_client import AnthropicProvider
from router import LLMRouter, LLMClient, ChatCompletions

__version__ = "1.0.0"
__author__ = "LLM Router Team"

__all__ = [
    "BaseProvider",
    "OpenAIProvider", 
    "AnthropicProvider",
    "LLMRouter",
    "LLMClient",
    "ChatCompletions"
] 