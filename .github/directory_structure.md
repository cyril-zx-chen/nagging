# Directory Structure

## Current Structure

```text
nagging/
├── apps/
│   ├── extension/          # Chrome Extension
│   │   └── src/
│   │       ├── popup/     # Extension UI
│   │       ├── content/   # Page integration
│   │       └── background/# Backend bridge
│   │
│   └── backend/           # Python Service
│       ├── src/
│       │   ├── api/       # FastAPI endpoints
│       │   ├── ai/        # AI service
│       │   └── cache/     # Caching
│       └── tests/         # Python tests
```

## Files To Be Added

### Extension Files

```text
apps/extension/
├── manifest.json        # Extension manifest
├── package.json        # Extension dependencies
├── webpack.config.js   # Build configuration
└── src/
    ├── popup/
    │   ├── index.html  # Popup UI
    │   ├── popup.ts    # Popup logic
    │   └── styles.css  # Popup styles
    ├── content/
    │   ├── index.ts    # Content script
    │   └── ui.ts       # UI components
    └── background/
        ├── index.ts    # Service worker
        └── api.ts      # Backend API
```

### Backend Files

```text
apps/backend/
├── pyproject.toml      # Python dependencies
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py   # API endpoints
│   │   └── models.py   # Data models
│   ├── ai/
│   │   ├── __init__.py
│   │   └── service.py  # OpenAI integration
│   └── cache/
│       ├── __init__.py
│       └── service.py  # Caching logic
└── tests/
    ├── test_api.py
    └── test_ai.py
```

## Root Files

```text
nagging/
├── package.json        # Root workspace config
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## Notes

- Clean, minimal structure
- Clear separation of extension and backend
- Each component has its own configuration
- Ready for implementation
