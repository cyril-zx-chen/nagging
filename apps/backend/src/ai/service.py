"""
AI Service for text suggestions using HuggingFace's Inference API.

This module provides an asynchronous service for generating text suggestions
using the HuggingFace Inference API. It supports both single-shot completions
and streaming responses.

Environment Variables:
    HF_API_KEY: HuggingFace API key
    HF_MODEL_URL: URL of the HuggingFace model to use
    AI_DO_SAMPLE: Whether to use sampling (default: true)
    AI_TOP_P: Top-p sampling parameter (default: 0.9)
    AI_STOP_TOKENS: Tokens to stop generation (default: \n,.,!,?)
    AI_RETURN_FULL_TEXT: Whether to return full text (default: false)
    AI_REQUEST_TIMEOUT: API request timeout in seconds (default: 30.0)
"""

from typing import AsyncGenerator, Optional
import os
import asyncio

import httpx
from pydantic import BaseModel, Field

from api.models import DEFAULT_MAX_TOKENS, MAX_TOKENS_LIMIT, DEFAULT_TEMPERATURE, MIN_TEMPERATURE, MAX_TEMPERATURE

# Load API request configuration
DO_SAMPLE = os.getenv("AI_DO_SAMPLE", "true").lower() == "true"
TOP_P = float(os.getenv("AI_TOP_P", "0.9"))
STOP_TOKENS = os.getenv("AI_STOP_TOKENS", "\\n,.,!,?").replace("\\n", "\n").split(",")
RETURN_FULL_TEXT = os.getenv("AI_RETURN_FULL_TEXT", "false").lower() == "true"
REQUEST_TIMEOUT = float(os.getenv("AI_REQUEST_TIMEOUT", "30.0"))

class TextContext(BaseModel):
    text: str = Field(..., description="The text to get suggestions for")
    max_tokens: int = Field(
        default=DEFAULT_MAX_TOKENS,
        ge=1,
        le=MAX_TOKENS_LIMIT,
        description=f"Maximum tokens to generate (1-{MAX_TOKENS_LIMIT})"
    )
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        ge=MIN_TEMPERATURE,
        le=MAX_TEMPERATURE,
        description=f"Sampling temperature ({MIN_TEMPERATURE}-{MAX_TEMPERATURE}). Lower values make the output more focused and deterministic"
    )

class AIService:
    def __init__(self):
        self.api_key = os.getenv("HF_API_KEY")
        self.api_url = os.getenv("HF_MODEL_URL", "https://api-inference.huggingface.co/models/microsoft/phi-2")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def _create_prompt(self, text: str) -> str:
        return f"""Assistant: I'll help you complete your text naturally. Here's how it continues:
Human: {text}
Assistant: Here's the continuation: {text}"""

    async def get_suggestion(self, context: TextContext) -> str:
        """Get a single completion suggestion."""
        async with httpx.AsyncClient() as client:
            prompt = self._create_prompt(context.text)
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": context.max_tokens,
                    "temperature": context.temperature,
                    "return_full_text": RETURN_FULL_TEXT,
                    "do_sample": DO_SAMPLE,
                    "top_p": TOP_P,
                    "stop": STOP_TOKENS
                }
            }
            
            response = await client.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=REQUEST_TIMEOUT
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
        """Stream completion suggestions word by word."""
        async with httpx.AsyncClient() as client:
            prompt = self._create_prompt(context.text)
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": context.max_tokens,
                    "temperature": context.temperature,
                    "return_full_text": RETURN_FULL_TEXT,
                    "do_sample": DO_SAMPLE,
                    "top_p": TOP_P
                }
            }
            
            response = await client.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=REQUEST_TIMEOUT
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
            for word in words:
                yield word + " "
                await asyncio.sleep(0.1)