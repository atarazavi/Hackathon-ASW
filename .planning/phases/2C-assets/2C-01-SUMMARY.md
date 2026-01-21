---
phase: 2C-assets
plan: 01
subsystem: documentation
tags: [guidelines, wcag, accessibility, design-system, ai-prompt]

# Dependency graph
requires:
  - phase: 2A-backend
    provides: Analyzer service that loads guidelines at runtime
provides:
  - GUIDELINES.md design standards document for AI analyzer
  - Customizable checklist-style criteria for LLM consumption
  - Measurable accessibility thresholds (WCAG 2.1/2.2)
affects: [03-integration, 04-polish]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Table-based guidelines for LLM parsing
    - Measurable criteria over prose descriptions
    - Customizable template with placeholder sections

key-files:
  created: []
  modified:
    - backend/guidelines/GUIDELINES.md

key-decisions:
  - "Table-based format: LLMs parse tables more reliably than prose paragraphs"
  - "Specific values: 4.5:1 contrast, 44px targets, not vague 'good contrast'"
  - "Custom Rules section: Placeholder for company-specific additions"

patterns-established:
  - "Guidelines structure: H2 sections map to analysis categories (States, A11y, Tokens, Responsiveness)"
  - "Example format: Each section ends with 'what the AI should flag' examples"

# Metrics
duration: 1min
completed: 2026-01-21
---

# Phase 2C Plan 01: GUIDELINES.md Summary

**Comprehensive design standards document with WCAG 2.1/2.2 thresholds, UI state requirements, and design token tables optimized for LLM consumption**

## Performance

- **Duration:** 1 min
- **Started:** 2026-01-21T12:55:02Z
- **Completed:** 2026-01-21T12:56:25Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments

- Created 204-line GUIDELINES.md with checklist-style criteria
- Covered all four analysis categories (UI States, Accessibility, Design Tokens, Responsiveness)
- Added Custom Rules section for company-specific extensions
- Used table-based format optimized for LLM parsing

## Task Commits

Each task was committed atomically:

1. **Task 1: Create guidelines directory and GUIDELINES.md** - `d0d23d8` (feat)

## Files Created/Modified

- `backend/guidelines/GUIDELINES.md` - Design standards for AI analyzer reference (replaced placeholder with comprehensive document)

## Decisions Made

- **Table-based format:** LLMs parse tables more reliably than prose paragraphs; all specifications use markdown tables
- **Specific measurable values:** Used exact thresholds (4.5:1 contrast, 44x44px targets, 4/8/16/24/32/48/64px spacing) instead of vague guidance
- **Custom Rules placeholder:** Included section with example format for company-specific rule additions

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- GUIDELINES.md ready for analyzer service to load at runtime
- File path matches existing `GUIDELINES_PATH` in `backend/app/services/analyzer.py`
- Integration testing in Phase 3 will verify guidelines are properly injected into LLM context

---
*Phase: 2C-assets*
*Completed: 2026-01-21*
