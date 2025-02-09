# Nagging - AI Text Suggestions

An AI-powered text suggestion tool that works anywhere you type.

## Project Structure

```text
nagging/
├── apps/
│   ├── extension/     # Chrome Extension (TypeScript)
│   └── backend/       # Python Backend (FastAPI)
```

## Backend Setup

### Prerequisites

- Python 3.11+
- Poetry (package manager)
- Redis (optional, for caching)
- HuggingFace API key

### Environment Setup

1. Navigate to the backend directory:

```bash
cd apps/backend
```

2. Create and activate virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies with Poetry:

```bash
pip install poetry
poetry install --no-root
```

4. Configure environment variables:

```bash
cp .env.example .env
# Edit .env and add your HuggingFace API key
```

### Environment Variables

The backend uses the following environment variables:

```bash
# HuggingFace API Configuration
HF_API_KEY=your_api_key_here
HF_MODEL_URL=https://api-inference.huggingface.co/models/microsoft/phi-2

# Frontend Configuration
FRONTEND_MAX_TOKENS=20        # Maximum tokens to generate
FRONTEND_TEMPERATURE=0.6      # Temperature for text generation
FRONTEND_DEBOUNCE_MS=1000    # Debounce time for suggestions

# AI Request Parameters
AI_DO_SAMPLE=true            # Whether to use sampling
AI_TOP_P=0.9                 # Top-p sampling parameter
AI_STOP_TOKENS=\n,.,!,?      # Tokens to stop generation
AI_RETURN_FULL_TEXT=false    # Whether to return full text
AI_REQUEST_TIMEOUT=30.0      # API request timeout in seconds
```

### Running the Server

Start the FastAPI server:

```bash
# Make sure you're in the src directory
cd src

# Run with Poetry
poetry run python main.py

# Or if already in Poetry shell
python main.py
```

### API Endpoints

- `/api/suggest` - Get text suggestions

  - POST request with JSON body:
    ```json
    {
      "text": "Your text here",
      "max_tokens": 20,
      "temperature": 0.6
    }
    ```

- `/api/suggest/stream` - Stream text suggestions
  - Same request format as `/api/suggest`
  - Returns Server-Sent Events (SSE)

### Development

The backend uses FastAPI with async support and integrates with HuggingFace's Inference API. Key components:

- `ai/service.py` - Core AI service for text suggestions
- `api/models.py` - Pydantic models for request/response
- `main.py` - FastAPI application and routes

### Development Tools

All development tools are configured in `pyproject.toml`:

- **Code Formatting**: black, isort
- **Linting**: ruff
- **Type Checking**: mypy
- **Testing**: pytest, pytest-asyncio

Run tools through Poetry:

```bash
# Format code
poetry run black .
poetry run isort .

# Type checking
poetry run mypy .

# Run tests
poetry run pytest
```

## Extension Setup

Coming soon...

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

TBD
