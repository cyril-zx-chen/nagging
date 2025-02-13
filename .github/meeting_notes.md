# Meeting Notes: Project Nagging Technical Stack

## Development Approach

- Focus on core functionality first
- Minimal viable infrastructure
- Quick iteration based on feedback
- No user accounts or data persistence in MVP

## 2024-02-06

### Architecture Decision

- Decided to use Python backend with FastAPI
  - Better AI/ML ecosystem
  - Native HuggingFace API support
  - More efficient text processing
  - Easier AI integration path
- Browser extension remains in TypeScript
  - Natural choice for browser integration
  - Good type safety
  - Rich extension APIs

### Technical Decisions

- Use Poetry for Python dependency management
  - Consistent dependency versions
  - Development tools integration (black, isort, ruff, mypy)
  - Virtual environment management
- Use HuggingFace's phi-2 model
  - Good balance of speed and quality
  - Free tier availability
  - Suitable for text completion
- Implement response caching for efficiency
- Use streaming responses for better UX
- Keep extension and backend clearly separated

### Next Steps (Prioritized)

1. Extension Development (MVP Priority)

   - Create extension structure
   - Implement text capture
   - Add suggestion UI
   - Connect to backend API

2. Basic Integration

   - Test end-to-end flow
   - Add basic error handling
   - Basic user settings

3. Post-MVP Improvements
   - Improve AI Service Robustness
     - Add retry logic
     - Add request rate limiting
   - Optimize Text Processing
     - Improve prompt engineering
     - Fine-tune response cleaning

## 2024-02-05

### Current State

- Project initialized with Nx monorepo
- Basic project structure in place
- Development environment configured
- Initial AI service implementation working

### Notes

- Focus on core text generation feature first
- Keep deployment simple
- Minimize infrastructure complexity
- Gather user feedback before adding features
