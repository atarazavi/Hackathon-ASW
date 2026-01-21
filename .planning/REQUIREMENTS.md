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

- [ ] **API-01**: Backend exposes `/analyze` POST endpoint
- [ ] **API-02**: Endpoint accepts design data payload with multiple frames (JSON array)
- [ ] **API-03**: Endpoint returns structured findings (JSON)
- [ ] **API-04**: Backend integrates with Azure OpenAI for analysis

### Analysis Agent

- [ ] **AGENT-01**: Agent detects missing UI states (loading, error, empty, disabled, hover)
- [ ] **AGENT-02**: Agent detects accessibility gaps (contrast, labels, focus states)
- [ ] **AGENT-03**: Agent detects design system violations (tokens, spacing, colors vs guidelines)
- [ ] **AGENT-04**: Agent detects responsiveness gaps (compares selected frames to identify missing breakpoints)
- [ ] **AGENT-05**: Agent uses provided guidelines document for reference

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

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| PLUG-01 | TBD | Pending |
| PLUG-02 | TBD | Pending |
| PLUG-03 | TBD | Pending |
| PLUG-04 | TBD | Pending |
| PLUG-05 | TBD | Pending |
| PLUG-06 | TBD | Pending |
| API-01 | TBD | Pending |
| API-02 | TBD | Pending |
| API-03 | TBD | Pending |
| API-04 | TBD | Pending |
| AGENT-01 | TBD | Pending |
| AGENT-02 | TBD | Pending |
| AGENT-03 | TBD | Pending |
| AGENT-04 | TBD | Pending |
| AGENT-05 | TBD | Pending |
| DEMO-01 | TBD | Pending |
| DEMO-02 | TBD | Pending |
| DEMO-03 | TBD | Pending |

**Coverage:**
- v1 requirements: 18 total
- Mapped to phases: 0
- Unmapped: 18 (pending roadmap)

---
*Requirements defined: 2026-01-21*
*Last updated: 2026-01-21 after initial definition*
