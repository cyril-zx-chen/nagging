import os
import sys
import pytest
from dotenv import load_dotenv

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.ai.service import AIService, TextContext

# Load environment variables
load_dotenv()

@pytest.mark.asyncio
async def test_ai_service_initialization():
    """Test that we can initialize the AI service."""
    service = AIService()
    assert service.api_url == "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    assert service.api_key == os.getenv("HF_API_KEY")

@pytest.mark.asyncio
async def test_get_suggestion():
    """Test getting a single suggestion."""
    service = AIService()
    context = TextContext(
        text="Python is a",
        max_tokens=5,
        temperature=0.7
    )
    
    suggestion = await service.get_suggestion(context)
    assert isinstance(suggestion, str)
    assert len(suggestion) > 0

@pytest.mark.asyncio
async def test_stream_suggestion():
    """Test streaming suggestions."""
    service = AIService()
    context = TextContext(
        text="Python is a",
        max_tokens=5,
        temperature=0.7
    )
    
    chunks = []
    async for chunk in service.stream_suggestion(context):
        chunks.append(chunk)
        
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)

if __name__ == "__main__":
    # Simple manual test
    import asyncio
    
    async def main():
        # Ensure HF_API_KEY is set
        if not os.getenv("HF_API_KEY"):
            print("Error: HF_API_KEY environment variable not set")
            return

        service = AIService()
        context = TextContext(text="Python is a")
        
        print("\nTesting single suggestion:")
        suggestion = await service.get_suggestion(context)
        print(f"Input: 'Python is a'")
        print(f"Suggestion: '{suggestion}'")
        
        print("\nTesting streaming suggestion:")
        print(f"Input: 'Python is a'")
        print("Streaming: ", end="", flush=True)
        async for chunk in service.stream_suggestion(context):
            print(chunk, end="", flush=True)
        print()

    asyncio.run(main()) 