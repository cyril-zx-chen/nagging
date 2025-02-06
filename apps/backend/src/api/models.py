from pydantic import BaseModel, Field

class SuggestionRequest(BaseModel):
    text: str = Field(..., description="The text to get suggestions for")
    max_tokens: int = Field(default=50, ge=1, le=100, description="Maximum tokens to generate")
    temperature: float = Field(
        default=0.7, ge=0, le=2, description="Sampling temperature"
    )

class SuggestionResponse(BaseModel):
    suggestion: str = Field(..., description="The generated suggestion")
    cached: bool = Field(default=False, description="Whether the response was cached") 