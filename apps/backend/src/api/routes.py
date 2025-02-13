from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import StreamingResponse
import os

from ai.service import AIService, TextContext
from cache.service import CacheService
from .models import SuggestionRequest, SuggestionResponse

router = APIRouter()

def get_ai_service():
    return AIService()

def get_cache_service():
    return CacheService()

@router.get("/config")
async def get_config():
    """Get frontend configuration."""
    return {
        "max_tokens": int(os.getenv("FRONTEND_MAX_TOKENS", "50")),
        "temperature": float(os.getenv("FRONTEND_TEMPERATURE", "0.7")),
        "debounce_ms": int(os.getenv("FRONTEND_DEBOUNCE_MS", "500"))
    }

@router.post("/suggest/test", response_model=SuggestionResponse)
async def get_suggestion_test() -> SuggestionResponse:
    suggestion = "Hello, world!"
    return SuggestionResponse(suggestion=suggestion, cached=False)

@router.post("/suggest", response_model=SuggestionResponse)
async def get_suggestion(
    request: SuggestionRequest,
    ai_service: AIService = Depends(get_ai_service),
    cache_service: CacheService = Depends(get_cache_service),
) -> SuggestionResponse:
    """Get a text suggestion."""
    # # Try cache first
    # if cached := await cache_service.get(
    #     request.text,
    #     max_tokens=request.max_tokens,
    #     temperature=request.temperature,
    # ):
    #     return SuggestionResponse(suggestion=cached, cached=True)

    print(f"------Request------: {request}")
    # Get new suggestion
    context = TextContext(
        text=request.text,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
    )
    suggestion = await ai_service.get_suggestion(context)

    print(f"------Suggestion------: {suggestion}")
    # # Cache the result
    # await cache_service.set(
    #     request.text,
    #     suggestion,
    #     max_tokens=request.max_tokens,
    #     temperature=request.temperature,
    # )

    return SuggestionResponse(suggestion=suggestion, cached=False)

@router.websocket("/suggest/stream")
async def stream_suggestion(
    websocket: WebSocket,
    ai_service: AIService = Depends(get_ai_service),
):
    """Stream text suggestions."""
    await websocket.accept()

    try:
        while True:
            # Receive and parse request
            data = await websocket.receive_json()
            request = SuggestionRequest(**data)

            # Stream suggestions
            context = TextContext(
                text=request.text,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
            )
            async for suggestion in ai_service.stream_suggestion(context):
                await websocket.send_text(suggestion)

    except Exception as e:
        await websocket.close(code=1001, reason=str(e))
