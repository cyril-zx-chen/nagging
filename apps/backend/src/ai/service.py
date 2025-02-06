from typing import AsyncGenerator, Optional
import os

from openai import AsyncOpenAI
from pydantic import BaseModel

class TextContext(BaseModel):
    text: str
    max_tokens: int = 50
    temperature: float = 0.7

class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.model = "gpt-3.5-turbo"

    async def get_suggestion(self, context: TextContext) -> str:
        """Get a single completion suggestion."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful text completion assistant. Provide brief, relevant continuations for the given text.",
                },
                {
                    "role": "user",
                    "content": f'Complete this text naturally: "{context.text}"',
                },
            ],
            max_tokens=context.max_tokens,
            temperature=context.temperature,
            stream=False,
        )
        return response.choices[0].message.content or ""

    async def stream_suggestion(
        self, context: TextContext
    ) -> AsyncGenerator[str, None]:
        """Stream completion suggestions."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful text completion assistant. Provide brief, relevant continuations for the given text.",
                },
                {
                    "role": "user",
                    "content": f'Complete this text naturally: "{context.text}"',
                },
            ],
            max_tokens=context.max_tokens,
            temperature=context.temperature,
            stream=True,
        )

        async for chunk in response:
            if content := chunk.choices[0].delta.content:
                yield content 