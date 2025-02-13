# Project Overview

## Goal

Build a lightweight text auto-generation AI tool that works anywhere you type.

## MVP Scope

- Browser extension with Python backend that:
  - Works in any text input context
  - Provides real-time text suggestions
  - Uses HuggingFace Inference API for text generation
  - Minimal UI with suggestion popup

## Technical Stack for MVP

### Core

- **Monorepo Structure**: Nx
- **Package Managers**:
  - Frontend: Yarn
  - Backend: Poetry

### Frontend (Chrome Extension)

- **Language**: TypeScript
- **Build Tool**: Webpack
- **Components**:
  - Popup UI
  - Content Scripts
  - Background Service

### Backend (Python Service)

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **AI Integration**: HuggingFace Inference API (phi-2 model)
- **Development Tools**:
  - Code Formatting: black, isort
  - Linting: ruff
  - Type Checking: mypy
  - Testing: pytest, pytest-asyncio
- **Caching**: Redis/SQLite

### Infrastructure

- **Development**: Local Python service
- **Production**: TBD (AWS/Vercel)

## Architecture Overview

### Data Flow

```
[Browser Tab] → [Content Script] → [Background Script] → [Python Backend] → [HuggingFace API]
     ↑              |                      ↑                    |              |
     └──────────────┴──────────────────────┴────────────[Cache]←──────────────┘
```

## Development Phases

### Phase 1: Basic Setup (Completed)

1. Create Python backend structure
2. Set up FastAPI with basic endpoint
3. Implement HuggingFace integration
4. Add basic caching

### Phase 2: Extension Development (Current)

1. Create extension structure
2. Implement text capture
3. Add suggestion display
4. Connect to backend

### Phase 3: MVP Improvements

1. Add basic error handling
2. Improve prompt engineering
3. Fine-tune response cleaning
4. Basic user settings

### Phase 4: Post-MVP Features

1. Improve service robustness
   - Add retry logic
   - Implement rate limiting
   - Advanced error handling
2. Advanced features
   - Enhanced prompt engineering
   - Better response cleaning
   - Advanced user customization
3. Implement streaming

### Supported LLMs

- HuggingFace phi-2 (Current)
- Other models TBD based on performance

## Development Tools

- **Version Control**: Git
- **Code Quality**:
  - Frontend:
    - ESLint
    - Prettier
    - TypeScript strict mode
  - Backend:
    - black/isort (formatting)
    - ruff (linting)
    - mypy (type checking)
    - pytest (testing)
- **Testing**:
  - Frontend: Jest
  - Backend: pytest, pytest-asyncio

## Current Status

1. Backend structure set up
2. Basic AI service working with phi-2 model
3. Initial text suggestion flow implemented
4. Development environment configured

## Next Steps

1. Start extension development
   - Set up extension structure
   - Implement text capture
   - Create suggestion UI
2. Connect extension to backend
   - Implement API client
   - Handle responses
   - Basic error handling
3. Test end-to-end flow
