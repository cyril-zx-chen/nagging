from typing import AsyncGenerator, Optional
import os
import json

import httpx
from pydantic import BaseModel

class TextContext(BaseModel):
    text: str
    max_tokens: int = 50  # Reduced max tokens
    temperature: float = 0.7  # Lower temperature for more focused completions

class AIService:
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        # Use a model better suited for natural text completion
        self.api_url = "https://api-inference.huggingface.co/models/microsoft/phi-2"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def get_suggestion(self, context: TextContext) -> str:
        """Get a single completion suggestion."""
        async with httpx.AsyncClient() as client:
            # Add a hint for natural completion
            prompt = f"{context.text} [continue naturally, be brief]"
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": context.max_tokens,
                    "temperature": context.temperature,
                    "return_full_text": False,
                    "do_sample": True,
                    "top_p": 0.9,
                    "stop": ["\n", ".", "!", "?"]  # Stop at natural breaks
                }
            }
            
            response = await client.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and result:
                    text = result[0].get("generated_text", "").strip()
                else:
                    text = result.get("generated_text", "").strip()
                # Clean up the response
                text = text.split('\n')[0]  # Take first line only
                text = text.split('.')[0]   # Take first sentence only
                return text.strip()
            else:
                raise Exception(f"API request failed: {response.text}")

    async def stream_suggestion(
        self, context: TextContext
    ) -> AsyncGenerator[str, None]:
        """Stream completion suggestions."""
        async with httpx.AsyncClient() as client:
            prompt = f"{context.text} [continue naturally, be brief]"
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": context.max_tokens,
                    "temperature": context.temperature,
                    "return_full_text": False,
                    "do_sample": True,
                    "top_p": 0.9,
                    "stop": ["\n", ".", "!", "?"]
                }
            }
            
            response = await client.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"API request failed: {response.text}")
            
            result = response.json()
            text = ""
            if isinstance(result, list) and result:
                text = result[0].get("generated_text", "").strip()
            else:
                text = result.get("generated_text", "").strip()
            
            # Clean and stream the text
            text = text.split('\n')[0]  # Take first line only
            text = text.split('.')[0]   # Take first sentence only
            words = text.split()
            
            # Add small delay between words for better readability
            for word in words:
                yield word + " "