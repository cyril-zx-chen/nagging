# Nagging - AI Text Suggestions

An AI-powered text suggestion tool that works anywhere you type.

## Project Structure

```
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

3. Install dependencies:

```bash
pip install poetry
poetry install --no-root
```

4. Configure environment variables:

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Running Tests

#### Quick Test

To run a simple manual test of the AI service:

```bash
python tests/test_ai.py
```

This will:

- Test single-shot completion
- Test streaming completion
- Print results to console

#### Full Test Suite

To run all tests with pytest:

```bash
pytest tests/ -v
```

For specific test files:

```bash
pytest tests/test_ai.py -v  # AI service tests
```

### Development

1. Start the FastAPI server:

```bash
# Coming soon
```

2. API endpoints:

- `/api/suggest` - Get text suggestions
- `/api/suggest/stream` - Stream text suggestions

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
