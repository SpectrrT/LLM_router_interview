
# LLM Router

A minimal Python package that provides a unified interface to multiple LLM providers, starting with OpenAI and Anthropic.

## Features

- **Modular Design**: Easy to extend with new providers
- **Unified Interface**: Same API for all providers
- **OpenAI-like Usage**: Familiar interface similar to OpenAI's client
- **Type Hints**: Full type support for better development experience
- **Error Handling**: Comprehensive error handling and validation

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd LLM_router_interview
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from router import LLMClient

# Initialize with OpenAI
openai_client = LLMClient("openai", "your-openai-api-key")

# Use OpenAI-like interface
response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello, world!"}],
    max_tokens=50,
    temperature=0.7
)

print(response['content'])
```

### Using Different Providers

```python
from router import LLMClient

# OpenAI
openai_client = LLMClient("openai", "your-openai-api-key")
openai_response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "What is AI?"}],
    max_tokens=100
)

# Anthropic
anthropic_client = LLMClient("anthropic", "your-anthropic-api-key")
anthropic_response = anthropic_client.chat.completions.create(
    model="claude-3-sonnet-20240229",
    messages=[{"role": "user", "content": "What is AI?"}],
    max_tokens=100
)
```

### Direct Router Usage

```python
from router import LLMRouter

# Create router instance
router = LLMRouter("openai", "your-openai-api-key")

# Send chat request
response = router.chat(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=50,
    temperature=0.7
)
```

## API Reference

### LLMClient

The main client class that provides an OpenAI-like interface.

```python
LLMClient(provider_name: str, api_key: str)
```

- `provider_name`: Either "openai" or "anthropic"
- `api_key`: Your API key for the provider

### LLMRouter

The router class that dispatches requests to the appropriate provider.

```python
LLMRouter(provider_name: str, api_key: str)
```

### BaseProvider

Abstract base class for all providers. Inherit from this to add new providers.

```python
class BaseProvider(ABC):
    def __init__(self, api_key: str)
    def chat(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]
```

## Supported Models

### OpenAI
- `gpt-3.5-turbo`
- `gpt-4`
- `gpt-4-turbo`
- And other OpenAI models

### Anthropic
- `claude-3-sonnet-20240229`
- `claude-3-opus-20240229`
- `claude-3-haiku-20240307`
- And other Anthropic models

## Response Format

All providers return a standardized response format:

```python
{
    'provider': 'openai',  # or 'anthropic'
    'model': 'gpt-3.5-turbo',
    'content': 'The response text...',
    'usage': {
        'prompt_tokens': 10,
        'completion_tokens': 20,
        'total_tokens': 30
    },
    'raw_response': <original_response_object>
}
```

## Environment Variables

You can set your API keys as environment variables:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

Then use them in your code:

```python
import os
from router import LLMClient

openai_client = LLMClient("openai", os.getenv("OPENAI_API_KEY"))
```

## Adding New Providers

To add a new provider, inherit from `BaseProvider`:

```python
from .base import BaseProvider

class NewProvider(BaseProvider):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        # Initialize your provider's client
    
    def chat(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        # Implement the chat method
        # Return standardized response format
        pass
```

Then update the `LLMRouter._create_provider()` method to include your new provider.

## Example Usage

See `example_usage.py` for comprehensive examples of how to use the package.

## Error Handling

The package includes comprehensive error handling:

- Invalid message format validation
- API key validation
- Provider-specific error handling
- Standardized error messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Changelog / Improvements

### July 2025: Major Improvements

- **Flexible Provider Initialization:** All providers now accept optional config parameters for future extensibility.
- **Stricter Validation:** Message validation enforces a non-empty list of dicts with only 'role' and 'content' keys, both non-empty strings.
- **Parameter Validation:** Providers validate allowed parameters before making API calls.
- **Model Name Validation:** Providers can validate model names for correctness.
- **Provider Registry:** Adding new providers is as simple as subclassing `BaseProvider` and updating the provider registry in `LLMRouter`.
- **Provider Metadata:** Each provider exposes a `provider_name` property for easier routing and metadata.
- **System Message Handling:** Anthropic provider now handles multiple system messages robustly.
- **Robust Error Handling:** All providers use clear, standardized error reporting and handle missing/empty fields gracefully.
- **OpenAI-style Client:** `LLMClient` supports extra provider config and is more robust.
- **Cleaner, More Extensible Design:** Easier to add new providers and maintain a clean, scalable codebase.
- **Improved Documentation:** README and docstrings updated to reflect new usage patterns, extensibility, and error handling.


## Why This Design?

This design was chosen to maximize extensibility, maintainability, and ease of use for both end users and future contributors:

- **Abstraction & Modularity:** By defining a strict `BaseProvider` interface, all providers must follow the same contract, making it easy to add new LLM providers with minimal risk of breaking the system.
- **Unified API:** The OpenAI-style interface (`LLMClient`) ensures that users can switch between providers with zero code changes, lowering the barrier to experimentation and adoption.
- **Validation & Error Handling:** Centralized validation and error handling make the library robust and safe for use in production and at scale.
- **Provider Registry:** The registry pattern in the router makes it trivial to add new providers—just register the class, no need to change core logic.
- **Standardized Responses:** All providers return a consistent response format, simplifying downstream usage and integration.
- **Documentation & Developer Experience:** Comprehensive docstrings, type hints, and a clear README make it easy for others to understand, use, and extend the library.

This approach balances flexibility (easy to add new models/providers) with safety (hard to misuse or break), and is inspired by best practices from both open-source libraries and production systems.

## License

This project is licensed under the MIT License.