# Requirements: Frontend Design Reviewer

**Defined:** 2026-01-21
**Core Value:** Catch design problems before they become code problems

## v1 Requirements

Requirements for hackathon demo. Each maps to roadmap phases.

### Figma Plugin

- [ ] **PLUG-01**: Designer can select one or multiple frames in Figma and trigger review
- [ ] **PLUG-02**: Plugin extracts design data (layers, styles, tokens) from all selected frames
- [ ] **PLUG-03**: Plugin calls backend API with extracted design data
- [ ] **PLUG-04**: Plugin displays structured findings in a results panel
- [ ] **PLUG-05**: Findings show severity level (critical/warning/info)
- [ ] **PLUG-06**: Findings show actionable recommendations

### Backend API

- [x] **API-01**: Backend exposes `/analyze` POST endpoint ✓
- [x] **API-02**: Endpoint accepts design data payload with multiple frames (JSON array) ✓
- [x] **API-03**: Endpoint returns structured findings (JSON) ✓
- [x] **API-04**: Backend integrates with Azure OpenAI for analysis ✓

### Analysis Agent

- [x] **AGENT-01**: Agent detects missing UI states (loading, error, empty, disabled, hover) ✓
- [x] **AGENT-02**: Agent detects accessibility gaps (contrast, labels, focus states) ✓
- [x] **AGENT-03**: Agent detects design system violations (tokens, spacing, colors vs guidelines) ✓
- [x] **AGENT-04**: Agent detects responsiveness gaps (compares selected frames to identify missing breakpoints) ✓
- [x] **AGENT-05**: Agent uses provided guidelines document for reference ✓

### Demo Assets

- [ ] **DEMO-01**: Sample design guidelines document exists (GUIDELINES.md)
- [ ] **DEMO-02**: Sample Figma design with intentional issues exists
- [ ] **DEMO-03**: Demo script documents the walkthrough flow

## v2 Requirements

Deferred to future. Not in current roadmap.

### Extended Analysis

- **EXT-01**: Agent suggests specific fixes, not just identifies problems
- **EXT-02**: Agent compares against real design system (not sample guidelines)
- **EXT-03**: Analysis includes component naming suggestions

### Integration

- **INT-01**: Jira integration for ticket review
- **INT-02**: VS Code MCP for developer workflow
- **INT-03**: Component code generation from designs

### Polish

- **POL-01**: Findings can be exported as markdown report
- **POL-02**: Findings can create Jira subtasks automatically
- **POL-03**: Historical review tracking

## Out of Scope

Explicitly excluded from hackathon demo.

| Feature | Reason |
|---------|--------|
| MCP server | Figma plugin is simpler, designer stays in tool |
| Jira integration | Adds complexity, not needed for design review demo |
| Code generation | Separate feature, tighter scope for hackathon |
| Real-time sync | Point-in-time analysis is sufficient |
| Production deployment | Local demo only |
| Real design system | Sample guidelines faster to create |

## Traceability

Which phases cover which requirements.

| Requirement | Phase | Status |
|-------------|-------|--------|
| PLUG-01 | Phase 2B | Pending |
| PLUG-02 | Phase 2B | Pending |
| PLUG-03 | Phase 2B | Pending |
| PLUG-04 | Phase 4 | Pending |
| PLUG-05 | Phase 4 | Pending |
| PLUG-06 | Phase 4 | Pending |
| API-01 | Phase 2A | Complete |
| API-02 | Phase 2A | Complete |
| API-03 | Phase 2A | Complete |
| API-04 | Phase 2A | Complete |
| AGENT-01 | Phase 2A | Complete |
| AGENT-02 | Phase 2A | Complete |
| AGENT-03 | Phase 2A | Complete |
| AGENT-04 | Phase 2A | Complete |
| AGENT-05 | Phase 2A | Complete |
| DEMO-01 | Phase 2C | Pending |
| DEMO-02 | Phase 2C | Pending |
| DEMO-03 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 18 total
- Mapped to phases: 18
- Unmapped: 0

---
*Requirements defined: 2026-01-21*
*Last updated: 2026-01-21 after roadmap creation*
