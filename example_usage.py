#!/usr/bin/env python3
"""
Example usage of the LLM Router package.

This file demonstrates how to use both OpenAI and Anthropic providers
with the same unified interface.
"""

from dotenv import load_dotenv
load_dotenv()
import os
from router import LLMClient, LLMRouter


def example_with_router():
    """Example using the LLMRouter directly."""
    print("=== Example using LLMRouter directly ===\n")
    
    # Example messages
    messages = [
        {"role": "user", "content": "What is the capital of France?"}
    ]
    
    # Get API keys from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    try:
        openai_router = LLMRouter("openai", openai_api_key)
        openai_response = openai_router.chat(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=50,
            temperature=0.7,
            top_p=1
        )
        
        print("OpenAI Response:")
        print(f"Provider: {openai_response['provider']}")
        print(f"Model: {openai_response['model']}")
        print(f"Content: {openai_response['content']}")
        print(f"Usage: {openai_response['usage']}")
        print()
        
    except Exception as e:
        print(f"OpenAI Error: {e}")
        print()
    
    try:
        anthropic_router = LLMRouter("anthropic", anthropic_api_key)
        anthropic_response = anthropic_router.chat(
            model="claude-3-haiku-20240307",
            messages=messages,
            max_tokens=50,
            temperature=0.7,
            top_p=1
        )
        
        print("Anthropic Response:")
        print(f"Provider: {anthropic_response['provider']}")
        print(f"Model: {anthropic_response['model']}")
        print(f"Content: {anthropic_response['content']}")
        print(f"Usage: {anthropic_response['usage']}")
        print()
        
    except Exception as e:
        print(f"Anthropic Error: {e}")
        print()


def example_with_client():
    """Example using the LLMClient with OpenAI-like interface."""
    print("=== Example using LLMClient (OpenAI-like interface) ===\n")
    
    # Example messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ]
    
    # Get API keys from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    try:
        openai_client = LLMClient("openai", openai_api_key)
        openai_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            temperature=0.7,
            top_p=1
        )
        
        print("OpenAI Response (Client Interface):")
        print(f"Provider: {openai_response['provider']}")
        print(f"Model: {openai_response['model']}")
        print(f"Content: {openai_response['content']}")
        print(f"Usage: {openai_response['usage']}")
        print()
        
    except Exception as e:
        print(f"OpenAI Error: {e}")
        print()
    
    try:
        anthropic_client = LLMClient("anthropic", anthropic_api_key)
        anthropic_response = anthropic_client.chat.completions.create(
            model="claude-3-haiku-20240307",
            messages=messages,
            max_tokens=100,
            temperature=0.7,
            top_p=1
        )
        
        print("Anthropic Response (Client Interface):")
        print(f"Provider: {anthropic_response['provider']}")
        print(f"Model: {anthropic_response['model']}")
        print(f"Content: {anthropic_response['content']}")
        print(f"Usage: {anthropic_response['usage']}")
        print()
        
    except Exception as e:
        print(f"Anthropic Error: {e}")
        print()


def example_with_environment_variables():
    """Example using API keys from environment variables."""
    print("=== Example using environment variables ===\n")
    
    # Example messages
    messages = [
        {"role": "user", "content": "What is the meaning of life?"}
    ]
    
    # Get API keys from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if openai_api_key:
        try:
            openai_client = LLMClient("openai", openai_api_key)
            openai_response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=50,
                temperature=0.7
            )
            
            print("OpenAI Response (from env):")
            print(f"Content: {openai_response['content']}")
            print()
            
        except Exception as e:
            print(f"OpenAI Error: {e}")
            print()
    else:
        print("OPENAI_API_KEY not found in environment variables")
        print()
    
    if anthropic_api_key:
        try:
            anthropic_client = LLMClient("anthropic", anthropic_api_key)
            anthropic_response = anthropic_client.chat.completions.create(
                model="claude-3-haiku-20240307",
                messages=messages,
                max_tokens=50,
                temperature=0.7
            )
            
            print("Anthropic Response (from env):")
            print(f"Content: {anthropic_response['content']}")
            print()
            
        except Exception as e:
            print(f"Anthropic Error: {e}")
            print()
    else:
        print("ANTHROPIC_API_KEY not found in environment variables")
        print()


if __name__ == "__main__":
    print("LLM Router Example Usage\n")
    print("Note: You need to add your API keys to run these examples successfully.\n")
    
    # Run examples
    example_with_router()
    example_with_client()
    example_with_environment_variables()
    
    print("=== Setup Instructions ===")
    print("1. Install required packages:")
    print("   pip install openai anthropic python-dotenv")
    print()
    print("2. Set your API keys in a .env file:")
    print("   OPENAI_API_KEY=your-openai-api-key")
    print("   ANTHROPIC_API_KEY=your-anthropic-api-key")
    print()
    print("3. Or set them in your environment before running the script.")
    print()
    print("4. Run the example:")
    print("   python example_usage.py") 