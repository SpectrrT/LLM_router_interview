#!/usr/bin/env python3
"""
Simple test file to verify the package structure and imports.
"""

def test_imports():
    """Test that all modules can be imported correctly."""
    try:
        from base import BaseProvider
        print("✓ BaseProvider imported successfully")
        
        from openai_client import OpenAIProvider
        print("✓ OpenAIProvider imported successfully")
        
        from anthropic_client import AnthropicProvider
        print("✓ AnthropicProvider imported successfully")
        
        from router import LLMRouter, LLMClient, ChatCompletions
        print("✓ Router classes imported successfully")
        
        print("\nAll imports successful! Package structure is correct.")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_abstract_class():
    """Test that BaseProvider is properly abstract."""
    from base import BaseProvider
    from abc import ABC
    
    # Check that BaseProvider is abstract
    assert issubclass(BaseProvider, ABC), "BaseProvider should inherit from ABC"
    print("✓ BaseProvider is properly abstract")


def test_provider_inheritance():
    """Test that providers inherit from BaseProvider."""
    from base import BaseProvider
    from openai_client import OpenAIProvider
    from anthropic_client import AnthropicProvider
    
    # Check inheritance
    assert issubclass(OpenAIProvider, BaseProvider), "OpenAIProvider should inherit from BaseProvider"
    assert issubclass(AnthropicProvider, BaseProvider), "AnthropicProvider should inherit from BaseProvider"
    print("✓ Provider inheritance is correct")


def test_router_creation():
    """Test router creation with valid providers."""
    from router import LLMRouter
    
    # Test with valid provider names
    try:
        # These will fail without API keys, but should not raise ValueError for provider name
        router1 = LLMRouter("openai", "dummy-key")
        print("✓ OpenAI router creation successful")
        
        router2 = LLMRouter("anthropic", "dummy-key")
        print("✓ Anthropic router creation successful")
        
    except ValueError as e:
        if "Unsupported provider" in str(e):
            print(f"✗ Router creation failed: {e}")
            return False
        else:
            # Expected to fail due to invalid API key, not provider name
            print("✓ Router creation with valid provider names successful")
    
    # Test with invalid provider name
    try:
        router3 = LLMRouter("invalid-provider", "dummy-key")
        print("✗ Should have raised ValueError for invalid provider")
        return False
    except ValueError as e:
        if "Unsupported provider" in str(e):
            print("✓ Correctly raised ValueError for invalid provider")
        else:
            print(f"✗ Unexpected error: {e}")
            return False
    
    return True


if __name__ == "__main__":
    print("Running LLM Router package tests...\n")
    
    # Run tests
    test_imports()
    print()
    
    test_abstract_class()
    print()
    
    test_provider_inheritance()
    print()
    
    test_router_creation()
    print()
    
    print("Package tests completed!")
