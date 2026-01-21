---
phase: 2A-backend
plan: 01
subsystem: api
tags: [fastapi, pydantic, azure-openai, async]

# Dependency graph
requires:
  - phase: 01-setup
    provides: FastAPI app skeleton with config.py and routers/review.py
provides:
  - Pydantic request models (DesignDataRequest, Frame, FrameLayer, TextNode)
  - Pydantic response models (AnalysisResult, Finding, Severity, FindingCategory)
  - POST /review/analyze endpoint skeleton
  - AsyncAzureOpenAI client lifecycle via lifespan
affects: [2A-02, 2B-plugin]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Lifespan context manager for async client initialization"
    - "app.state for sharing client/settings across requests"
    - "str,Enum pattern for JSON-serializable enums"

key-files:
  created:
    - backend/app/models/__init__.py
    - backend/app/models/request.py
    - backend/app/models/response.py
  modified:
    - backend/app/main.py
    - backend/app/config.py
    - backend/app/routers/review.py

key-decisions:
  - "API version updated to 2024-10-01-preview for structured outputs support"
  - "Removed lru_cache get_settings() in favor of settings on app.state"

patterns-established:
  - "Lifespan: Initialize shared async clients at startup, access via request.app.state"
  - "Models: Use | None instead of Optional for OpenAI structured output compatibility"

# Metrics
duration: 2min
completed: 2026-01-21
---

# Phase 2A Plan 01: API Contract and Client Infrastructure Summary

**Pydantic request/response models with /analyze endpoint skeleton and AsyncAzureOpenAI lifespan initialization**

## Performance

- **Duration:** 2 min
- **Started:** 2026-01-21T12:18:12Z
- **Completed:** 2026-01-21T12:19:44Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments
- Created Pydantic models for design data (DesignDataRequest, Frame, FrameLayer, TextNode)
- Created Pydantic response models with severity/category enums (AnalysisResult, Finding)
- Wired up POST /review/analyze endpoint with stub response
- Implemented AsyncAzureOpenAI client lifecycle via FastAPI lifespan

## Task Commits

Each task was committed atomically:

1. **Task 1: Create Pydantic models for request and response** - `9f5bd8b` (feat)
2. **Task 2: Update main.py with lifespan and wire endpoint** - `63dd143` (feat)

## Files Created/Modified
- `backend/app/models/__init__.py` - Re-exports all model classes
- `backend/app/models/request.py` - DesignDataRequest, Frame, FrameLayer, TextNode
- `backend/app/models/response.py` - AnalysisResult, Finding, Severity, FindingCategory enums
- `backend/app/main.py` - Added lifespan, removed lru_cache settings, include router
- `backend/app/config.py` - Updated API version to 2024-10-01-preview
- `backend/app/routers/review.py` - POST /analyze endpoint with stub response

## Decisions Made
- Updated Azure OpenAI API version from `2024-02-15-preview` to `2024-10-01-preview` for structured outputs support
- Removed `get_settings()` with `@lru_cache` - settings now stored on `app.state` via lifespan
- Used `| None` syntax instead of `Optional[]` for better OpenAI structured output compatibility

## Deviations from Plan
None - plan executed exactly as written.

## Issues Encountered
- macOS lacks `timeout` command - used background process with sleep instead for endpoint testing

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- API contract established - Plan 02 can implement real analysis logic
- AsyncAzureOpenAI client accessible via `request.app.state.openai_client`
- Response models ready for LLM structured output parsing

---
*Phase: 2A-backend*
*Completed: 2026-01-21*
