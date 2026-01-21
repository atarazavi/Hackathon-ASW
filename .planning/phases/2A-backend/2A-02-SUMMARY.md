---
phase: 2A-backend
plan: 02
subsystem: api
tags: [azure-openai, structured-outputs, llm-agent, design-analysis, pydantic]

# Dependency graph
requires:
  - phase: 2A-01
    provides: FastAPI app, AsyncAzureOpenAI client, Pydantic models, /review/analyze stub
provides:
  - Azure OpenAI analysis agent with structured outputs
  - Design review across 4 categories (states, a11y, design system, responsiveness)
  - GUIDELINES.md placeholder for agent context
  - Error handling for rate limits (429) and API errors (502)
affects: [2A-03, 2C-assets, phase-3, phase-4]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - beta.chat.completions.parse() for structured outputs
    - Pydantic model as response_format for guaranteed JSON schema
    - Guidelines loaded from file with request override

key-files:
  created:
    - backend/guidelines/GUIDELINES.md
    - backend/app/services/__init__.py
    - backend/app/services/analyzer.py
  modified:
    - backend/app/routers/review.py

key-decisions:
  - "Comprehensive SYSTEM_PROMPT with 4 categories and severity levels"
  - "temperature=0.2 for consistent analysis"
  - "Guidelines file path relative to analyzer.py using Path(__file__)"
  - "Graceful FileNotFoundError handling for missing guidelines"

patterns-established:
  - "analyzer.py: SYSTEM_PROMPT constant, async analyze_design function"
  - "router: try/except for RateLimitError and APIError with specific HTTP codes"

# Metrics
duration: 1min
completed: 2026-01-21
---

# Phase 2A Plan 02: Azure OpenAI Analyzer Agent Summary

**Implemented Azure OpenAI analysis agent with structured outputs, detecting issues across UI states, accessibility, design system, and responsiveness categories**

## Performance

- **Duration:** 1 min
- **Started:** 2026-01-21T12:21:14Z
- **Completed:** 2026-01-21T12:22:28Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments

- Created analyzer service using `beta.chat.completions.parse()` for guaranteed structured JSON
- Comprehensive SYSTEM_PROMPT covering all four analysis categories with specific items
- Placeholder GUIDELINES.md with UI states, a11y requirements, design system, and breakpoints
- Error handling for Azure OpenAI rate limits (429) and API errors (502)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create placeholder guidelines and analyzer service** - `172e292` (feat)
2. **Task 2: Wire analyzer to endpoint with error handling** - `3b094b4` (feat)

## Files Created/Modified

- `backend/guidelines/GUIDELINES.md` - Placeholder design guidelines (UI states, a11y, spacing, breakpoints)
- `backend/app/services/__init__.py` - Exports analyze_design function
- `backend/app/services/analyzer.py` - Azure OpenAI analyzer with structured outputs
- `backend/app/routers/review.py` - Updated endpoint with real analysis and error handling

## Decisions Made

1. **Comprehensive SYSTEM_PROMPT:** Includes explicit enumeration of all states (loading, error, empty, disabled, hover, focus, pressed), accessibility checks (4.5:1 contrast, labels, focus, 44px touch targets), design system (4px grid), and responsiveness (breakpoints).

2. **Temperature 0.2:** Lower temperature for more consistent analysis across runs.

3. **File-relative GUIDELINES_PATH:** Uses `Path(__file__).parent.parent.parent / "guidelines"` to work regardless of working directory.

4. **Graceful guidelines handling:** FileNotFoundError returns empty string rather than failing, allowing override via request.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required. (Azure OpenAI credentials configured in Plan 01)

## Next Phase Readiness

- Backend API complete with real Azure OpenAI analysis
- Ready for Phase 2B (plugin integration) to call `/review/analyze`
- Phase 2C will enhance GUIDELINES.md with full design standards
- All 9 Phase 2A requirements satisfied:
  - API-01: POST /review/analyze endpoint
  - API-02: Request body matches plugin output
  - API-03: Response contains categorized findings
  - API-04: Findings have severity and recommendations
  - AGENT-01: Detects missing UI states
  - AGENT-02: Detects accessibility gaps
  - AGENT-03: Detects design system violations
  - AGENT-04: Detects responsiveness gaps
  - AGENT-05: Uses guidelines document for reference

---
*Phase: 2A-backend*
*Completed: 2026-01-21*
