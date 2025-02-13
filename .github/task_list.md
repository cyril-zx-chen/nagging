# Task List

## Current Status (2024-02-06)

- [x] Choose tech stack for MVP
  - [x] Python + FastAPI for backend
  - [x] TypeScript for extension
  - [x] HuggingFace API for AI
- [x] Design new architecture
  - [x] Document component structure
  - [x] Plan data flow
  - [x] Define development phases
- [x] Set up Python Backend
  - [x] Create project structure
  - [x] Set up FastAPI configuration
  - [x] Create initial service files
  - [x] Setting up development environment
    - [x] Create virtual environment (.venv)
    - [x] Install dependencies
    - [x] Configure HuggingFace API
    - [x] Test basic imports

## In Progress

- [ ] Create Extension MVP
  - [ ] Set up extension project
    - [ ] Initialize TypeScript project
    - [ ] Configure Webpack
    - [ ] Set up ESLint and Prettier
  - [ ] Implement core components
    - [ ] Content script for text capture
    - [ ] Background service for API communication
    - [ ] Popup UI for settings
  - [ ] Basic functionality
    - [ ] Text input detection
    - [ ] API client for backend
    - [ ] Suggestion display
    - [ ] Basic error handling

## Next Up

- [ ] MVP Testing & Integration

  - [ ] End-to-end testing
  - [ ] Basic user settings
  - [ ] Performance testing
  - [ ] Bug fixes

- [ ] Post-MVP Improvements
  - [ ] Improve AI Service Robustness
    - [ ] Add error handling for API timeouts
    - [ ] Implement retry logic
    - [ ] Add request rate limiting
  - [ ] Optimize Text Processing
    - [ ] Improve prompt engineering
    - [ ] Fine-tune response cleaning
    - [ ] Add context awareness

## Environment Setup Details

```text
Location: /Users/cyrilchen/Documents/03_Self/nagging/nagging/apps/backend
Virtual Env: .venv
Current Status: Basic AI service working with HuggingFace phi-2 model
Next Action: Set up Chrome extension project
```

## Post-MVP Features

- [ ] User accounts and authentication
- [ ] Advanced caching strategies
- [ ] Additional AI providers integration
- [ ] Advanced prompt customization
- [ ] Usage analytics
- [ ] Desktop app version

## Removed from MVP Scope

- ~~Next.js backend~~
- ~~Complex state management~~
- ~~User authentication~~
- ~~Data persistence~~
- ~~Multiple AI providers (initially)~~
- ~~Advanced error handling~~
- ~~Service robustness features~~
