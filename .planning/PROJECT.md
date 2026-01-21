# Frontend Accelerator MCP

## What This Is

An AI-powered assistant that improves frontend delivery quality by catching problems earlier and helping teams move from design and tickets to implementation faster. It's a Python backend running multiple agents, exposed as an MCP server for VS Code Copilot integration.

## Core Value

Developers get implementation-ready Angular components from a single command — no back-and-forth on missing requirements, design gaps, or pattern inconsistencies.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Jira ticket analysis: fetch ticket by ID, extract requirements, identify linked Figma designs
- [ ] Figma design analysis: extract component structure, identify missing states (loading/error/empty), check accessibility gaps
- [ ] Workspace pattern analysis: read current Angular project, infer component patterns, coding conventions
- [ ] Angular component generation: produce implementation-ready code matching workspace patterns
- [ ] MCP server: expose agents as tools callable from VS Code Copilot
- [ ] End-to-end flow: ticket ID → enriched spec + generated component

### Out of Scope

- Jira write access (creating subtasks automatically) — read-only for hackathon demo
- Figma plugin — stretch goal only, not primary demo
- Jira automation triggers — stretch goal only
- Code reviewer agent — nice to have, not in primary flow
- Production deployment — local demo only

## Context

**Hackathon challenge** with specific success criteria:
1. Demonstrate at least one end-to-end flow with real design + ticket data
2. Integrate with common design and ticketing tools (read access)
3. Provide a usable interface (MCP in VS Code)
4. Produce outputs that are genuinely actionable for developers

**Team composition (6 people, 3-4 hours):**
- 1 Full-stack developer
- 2 Frontend developers
- 2 Designers
- 1 BA
- 4 people have access to coding agents

**Integrations available:**
- Jira Cloud API (user-level access, read-only)
- Figma API (can build plugins)
- Azure OpenAI (LLM provider)

**Target output:** Angular components (not React) matching patterns from whatever repo is open in VS Code when agent is invoked.

## Constraints

- **Timeline**: 3-4 hours total build time
- **LLM**: Azure OpenAI (company standard)
- **Backend**: Python
- **Interface**: MCP server for VS Code Copilot
- **Demo**: Needs real Jira ticket + Figma design data

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| MCP calls Python backend API | Keeps MCP server thin, agent logic centralized | — Pending |
| Focus on Ticket→Component flow | Highest demo impact, covers most agents | — Pending |
| Angular over React | Matches company's existing codebase | — Pending |
| Sample guidelines for demo | Faster than extracting real company docs | — Pending |
| Skip Figma plugin for core demo | Time constraint, VS Code is dev's natural workspace | — Pending |

## Team Workstream Plan

**Phase 0: Setup (30 min, everyone together)**
- Project scaffolding (Python backend, MCP server structure)
- API keys configured (Azure OpenAI, Jira, Figma)
- Git repo, basic structure, verify everyone can run locally

**Then branch out:**

| Person | Role | Primary Task | Deliverable |
|--------|------|--------------|-------------|
| Full-stack | Backend lead | Agent orchestration + Azure OpenAI integration | Working agent pipeline |
| Frontend 1 | MCP server | MCP implementation + VS Code testing | Callable MCP tools |
| Frontend 2 | Integrations | Jira API + Figma API clients | Data fetching working |
| Designer 1 | Guidelines | Sample design guidelines document | Guidelines.md for agents |
| Designer 2 | Demo assets | Sample Figma designs, test scenarios | Demo-ready designs |
| BA | Demo prep | Sample Jira tickets, test cases, demo script | End-to-end test data |

**Integration points:**
- Frontend 2's API clients → Full-stack's agent pipeline
- Full-stack's agents → Frontend 1's MCP server
- Designer 1's guidelines → Full-stack's agent prompts
- BA's test data → Everyone's integration testing

**Last hour:** Integration, end-to-end testing, demo rehearsal

---
*Last updated: 2026-01-21 after initialization*
