# Frontend Design Reviewer

## What This Is

A Figma plugin powered by AI that reviews designs for completeness before developer handoff. Designers select a frame, click review, and get structured findings on missing states, accessibility gaps, design system violations, and responsiveness issues. Python backend uses Azure OpenAI to analyze designs against guidelines.

## Core Value

Catch design problems before they become code problems — designers get actionable feedback in Figma, not during code review.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Figma plugin: select frame, trigger review, display findings
- [ ] Python backend: receive design data, analyze with Azure OpenAI, return structured findings
- [ ] Missing states detection: identify absent loading, error, empty, disabled, hover states
- [ ] Accessibility gap detection: contrast issues, missing labels, focus state gaps
- [ ] Design system violation detection: inconsistent tokens, spacing, colors vs guidelines
- [ ] Responsiveness check: mobile/tablet breakpoint coverage gaps
- [ ] Sample guidelines: document defining what to check against

### Out of Scope

- MCP server / VS Code integration — not needed for design review flow
- Jira integration — future scope, not this demo
- Component code generation — future scope
- Code review agent — future scope
- Production deployment — local demo only
- Real-time Figma sync — point-in-time analysis only

## Context

**Hackathon challenge** with specific success criteria:
1. Demonstrate at least one end-to-end flow with real design data
2. Integrate with common design tools (Figma)
3. Provide a usable interface (Figma plugin)
4. Produce outputs that are genuinely actionable for designers

**Team composition (6 people, 3-4 hours):**
- 1 Full-stack developer
- 2 Frontend developers
- 2 Designers
- 1 BA
- 4 people have access to coding agents

**Integrations:**
- Figma Plugin API (build and run plugins)
- Azure OpenAI (LLM provider for analysis)

**Target output:** Structured design review findings with severity levels and recommendations, displayed directly in Figma.

## Constraints

- **Timeline**: 3-4 hours total build time
- **LLM**: Azure OpenAI (company standard)
- **Backend**: Python
- **Interface**: Figma plugin
- **Demo**: Needs real Figma design data

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Figma plugin over MCP/VS Code | Designer stays in their tool, simpler demo flow | — Pending |
| Focus on design review only | Tighter scope for 3-4 hours, complete demo possible | — Pending |
| Direct API calls (no MCP layer) | Fewer moving parts, faster to build | — Pending |
| Sample guidelines for demo | Faster than extracting real company docs | — Pending |
| Point-in-time analysis | Avoid complexity of real-time sync | — Pending |

## Team Workstream Plan

**Phase 0: Setup (30 min, everyone together)**
- Project scaffolding (Python backend, Figma plugin boilerplate)
- Azure OpenAI API key configured and tested
- Git repo, basic structure, verify plugin loads in Figma

**Then branch out:**

| Person | Role | Primary Task | Deliverable |
|--------|------|--------------|-------------|
| Full-stack | Backend lead | Python API + Azure OpenAI analysis agent | `/analyze` endpoint that returns findings |
| Frontend 1 | Plugin logic | Figma plugin: extract design data, call backend | Working plugin that sends data |
| Frontend 2 | Plugin UI | Figma plugin: results display panel | Findings rendered in plugin UI |
| Designer 1 | Guidelines | Sample design guidelines document | GUIDELINES.md for agent prompts |
| Designer 2 | Demo assets | Sample Figma designs with intentional issues | Designs that trigger findings |
| BA | Demo prep | Test scenarios, demo script, edge cases | Rehearsed demo flow |

**Integration points:**
- Frontend 1's plugin → Full-stack's backend API
- Designer 1's guidelines → Full-stack's agent prompts
- Designer 2's test designs → Everyone's integration testing

**Last hour:** Integration, end-to-end testing, demo rehearsal

---
*Last updated: 2026-01-21 after scope refinement (design review via Figma plugin)*
