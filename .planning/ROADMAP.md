# Roadmap: Frontend Design Reviewer

## Overview

Build a Figma plugin that reviews designs for completeness before developer handoff. Four phases designed for parallel team execution: setup together, then three parallel workstreams (backend, plugin, assets), followed by integration and demo rehearsal. Optimized for 6 people working 3-4 hours.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3, 4): Planned milestone work
- Decimal phases (e.g., 2.1): Urgent insertions if needed

Phases 2A, 2B, 2C execute in parallel (different team members).

- [ ] **Phase 1: Setup** - Project scaffolding and environment verification
- [ ] **Phase 2A: Backend** - Python API with Azure OpenAI analysis agent
- [ ] **Phase 2B: Plugin** - Figma plugin data extraction and API integration
- [ ] **Phase 2C: Assets** - Guidelines document and demo test designs
- [ ] **Phase 3: Integration** - Connect plugin to backend, end-to-end flow
- [ ] **Phase 4: Demo** - Results UI, demo script, rehearsal

## Phase Details

### Phase 1: Setup
**Goal**: All team members have working environments and can build/test their components
**Depends on**: Nothing (first phase)
**Requirements**: None (foundational)
**Success Criteria** (what must be TRUE):
  1. Python backend runs locally with Azure OpenAI connection verified
  2. Figma plugin boilerplate loads in Figma (shows plugin window)
  3. Git repo initialized with folder structure for backend/plugin/docs
**Plans**: 2 plans

**Team**: Everyone (30 min)

Plans:
- [ ] 01-01-PLAN.md — Repository structure and Python backend scaffolding
- [ ] 01-02-PLAN.md — Figma plugin boilerplate with UI window

---

### Phase 2A: Backend
**Goal**: Backend can analyze design data and return structured findings
**Depends on**: Phase 1
**Requirements**: API-01, API-02, API-03, API-04, AGENT-01, AGENT-02, AGENT-03, AGENT-04, AGENT-05
**Success Criteria** (what must be TRUE):
  1. POST /analyze endpoint accepts JSON payload with design data
  2. Endpoint returns structured findings JSON with severity and recommendations
  3. Azure OpenAI analyzes for states, a11y, design system, responsiveness
  4. Agent uses guidelines document for reference during analysis
**Plans**: TBD

**Team**: Full-stack developer

Plans:
- [ ] 2A-01: API endpoint and Azure OpenAI integration
- [ ] 2A-02: Analysis agent prompts and finding structure

---

### Phase 2B: Plugin
**Goal**: Plugin can extract design data and call backend API
**Depends on**: Phase 1
**Requirements**: PLUG-01, PLUG-02, PLUG-03
**Success Criteria** (what must be TRUE):
  1. Designer can select one or multiple frames and click "Review"
  2. Plugin extracts layers, styles, and tokens from selected frames
  3. Plugin successfully POSTs extracted data to backend /analyze endpoint
**Plans**: TBD

**Team**: Frontend developers 1 and 2

Plans:
- [ ] 2B-01: Frame selection and data extraction
- [ ] 2B-02: API client and backend communication

---

### Phase 2C: Assets
**Goal**: Demo materials exist for testing and presentation
**Depends on**: Phase 1
**Requirements**: DEMO-01, DEMO-02
**Success Criteria** (what must be TRUE):
  1. GUIDELINES.md exists with design standards for agent reference
  2. Sample Figma design exists with intentional issues (missing states, a11y gaps, etc.)
  3. Test designs cover all four analysis categories
**Plans**: TBD

**Team**: Designers 1 and 2

Plans:
- [ ] 2C-01: Guidelines document
- [ ] 2C-02: Test designs with intentional issues

---

### Phase 3: Integration
**Goal**: End-to-end flow works: select frames, review, see findings
**Depends on**: Phase 2A, Phase 2B, Phase 2C
**Requirements**: None (integration of existing)
**Success Criteria** (what must be TRUE):
  1. Plugin sends real design data to running backend
  2. Backend returns analysis findings based on guidelines
  3. Round-trip completes within reasonable time (< 30 seconds)
  4. Findings correctly identify issues in test designs
**Plans**: TBD

**Team**: Full-stack + Frontend devs

Plans:
- [ ] 03-01: Connect plugin to backend
- [ ] 03-02: End-to-end testing with test designs

---

### Phase 4: Demo
**Goal**: Complete demo-ready experience with polished results display
**Depends on**: Phase 3
**Requirements**: PLUG-04, PLUG-05, PLUG-06, DEMO-03
**Success Criteria** (what must be TRUE):
  1. Findings display in clear panel within Figma plugin
  2. Severity levels (critical/warning/info) are visually distinct
  3. Each finding shows actionable recommendation
  4. Demo script documents complete walkthrough flow
  5. Demo rehearsed at least once successfully
**Plans**: TBD

**Team**: Everyone (BA leads demo prep)

Plans:
- [ ] 04-01: Results UI panel
- [ ] 04-02: Demo script and rehearsal

## Progress

**Execution Order:**
Phase 1 (all) -> Phase 2A/2B/2C (parallel) -> Phase 3 -> Phase 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Setup | 0/2 | Planned | - |
| 2A. Backend | 0/2 | Not started | - |
| 2B. Plugin | 0/2 | Not started | - |
| 2C. Assets | 0/2 | Not started | - |
| 3. Integration | 0/2 | Not started | - |
| 4. Demo | 0/2 | Not started | - |

## Coverage

All 18 v1 requirements mapped:

| Category | Requirements | Phase |
|----------|--------------|-------|
| Backend API | API-01, API-02, API-03, API-04 | 2A |
| Analysis Agent | AGENT-01, AGENT-02, AGENT-03, AGENT-04, AGENT-05 | 2A |
| Plugin Core | PLUG-01, PLUG-02, PLUG-03 | 2B |
| Plugin UI | PLUG-04, PLUG-05, PLUG-06 | 4 |
| Demo Assets | DEMO-01, DEMO-02 | 2C |
| Demo Script | DEMO-03 | 4 |

**Total:** 18/18 requirements mapped
