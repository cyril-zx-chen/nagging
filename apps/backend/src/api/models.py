import os
from pydantic import BaseModel, Field

# Load configuration from environment variables
DEFAULT_MAX_TOKENS = int(os.getenv("AI_DEFAULT_MAX_TOKENS", "50"))
MAX_TOKENS_LIMIT = int(os.getenv("AI_MAX_TOKENS_LIMIT", "200"))
DEFAULT_TEMPERATURE = float(os.getenv("AI_DEFAULT_TEMPERATURE", "0.7"))
MIN_TEMPERATURE = float(os.getenv("AI_MIN_TEMPERATURE", "0.1"))
MAX_TEMPERATURE = float(os.getenv("AI_MAX_TEMPERATURE", "2.0"))

class SuggestionRequest(BaseModel):
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

class SuggestionResponse(BaseModel):
    suggestion: str = Field(..., description="The generated suggestion")
    cached: bool = Field(default=False, description="Whether the response was cached")