from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import StreamingResponse

from ..ai.service import AIService, TextContext
from ..cache.service import CacheService
from .models import SuggestionRequest, SuggestionResponse

router = APIRouter()

def get_ai_service():
    return AIService()

def get_cache_service():
    return CacheService()

@router.post("/suggest", response_model=SuggestionResponse)
async def get_suggestion(
    request: SuggestionRequest,
    ai_service: AIService = Depends(get_ai_service),
    cache_service: CacheService = Depends(get_cache_service),
) -> SuggestionResponse:
    """Get a text suggestion."""
    # Try cache first
    if cached := await cache_service.get(
        request.text,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
    ):
        return SuggestionResponse(suggestion=cached, cached=True)

    # Get new suggestion
    context = TextContext(
        text=request.text,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
    )
    suggestion = await ai_service.get_suggestion(context)

    # Cache the result
    await cache_service.set(
        request.text,
        suggestion,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
    )

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