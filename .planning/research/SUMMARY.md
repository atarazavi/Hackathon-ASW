# Project Research Summary

**Project:** Frontend Accelerator MCP Server
**Domain:** AI-Powered Design-to-Code Workflow
**Researched:** 2026-01-21
**Confidence:** HIGH

## Executive Summary

This hackathon project builds an MCP (Model Context Protocol) server that orchestrates AI agents to accelerate Angular frontend development. The core workflow takes a Jira ticket ID, fetches requirements and linked Figma designs, analyzes both through specialized agents, and generates implementation-ready Angular component code. The research strongly recommends a **vanilla Python approach** using the official MCP SDK (FastMCP) with direct Azure OpenAI calls rather than heavy agent frameworks. For a 3-4 hour hackathon, framework learning curves (30-60 minutes) would consume too much of the available time.

The recommended architecture uses **HTTP REST communication** between a thin MCP server and a Python backend running FastAPI. This enables parallel development where 6 team members can work independently on modular components (MCP server, Jira client, Figma client, three specialized agents). The MCP server connects to VS Code Copilot via stdio transport while calling the backend over HTTP, giving clean team boundaries and easy testability with curl/Postman.

The critical risks center on **API authentication and rate limits**. Stdout pollution will completely break MCP (all logging must go to stderr). Figma Starter plans have brutal rate limits (6 requests/month for non-owned files), Azure OpenAI 429 errors can halt demos, and Jira authentication has multiple traps (SSO never works, API tokens required). Mitigation: test all API auth in the first 30 minutes, cache responses aggressively, and have pre-generated fallback outputs for the demo.

## Key Findings

### Recommended Stack

Use minimal dependencies for maximum hackathon velocity. The official MCP SDK's FastMCP decorator pattern allows tool definitions in 3 lines of code. Azure OpenAI integration uses the standard `openai` library with the `AzureOpenAI` class.

**Core technologies:**
- `mcp[cli]>=1.25,<2` (MCP Server) - Official Anthropic SDK with FastMCP for simple tool definitions
- `openai>=2.15.0` (LLM Integration) - AzureOpenAI class provides identical API to OpenAI
- `httpx` (HTTP Client) - Async-native, already an openai dependency
- `python-dotenv` (Config) - Load API keys from .env
- `pydantic>=2.0` (Data Validation) - Structured inputs/outputs for agents
- `fastapi` (Backend) - Simple REST API for backend services

**Why NOT frameworks:** Microsoft Agent Framework is beta, OpenAI Agents SDK adds unnecessary abstraction, LangChain/LangGraph have massive overhead. Vanilla Python classes with async functions are faster to write and debug.

### Expected Features

**Must have (table stakes):**
- `accelerate` - End-to-end: ticket ID to generated component (the demo money shot)
- `analyze_ticket` - Fetch Jira ticket, extract structured requirements
- `analyze_design` - Fetch Figma design, identify component structure and gaps
- `generate_component` - Generate Angular files matching workspace patterns

**Should have (competitive):**
- `review_code` - Check generated code against workspace patterns (high demo impact)
- `get_workspace_patterns` - Extract coding patterns from current project

**Defer (v2+):**
- Jira write access (risk of polluting real projects)
- Full Figma plugin (time-intensive distribution)
- Multi-file refactoring (scope creep)
- Real-time design sync (complex state management)
- Production error handling (overkill for demo)

**Leverage existing ecosystem:** Figma MCP Server, Atlassian MCP Server, Angular CLI MCP Server, and ESLint MCP Server are all production-ready. Consider delegating to these rather than reimplementing.

### Architecture Approach

Use a "Thin MCP, Fat Backend" pattern. The MCP server contains zero business logic, only tool schemas and HTTP calls to the backend. All agent logic lives in Python, making it easy to test independently. Communication uses HTTP REST between MCP server and FastAPI backend, while VS Code connects to MCP server via stdio.

**Major components:**
1. **MCP Server** - Tool definitions, HTTP proxying to backend (Person 1)
2. **FastAPI Backend** - Endpoint routing, agent orchestration (Full-stack lead)
3. **Integrations Module** - Jira and Figma API clients (Person 2)
4. **Ticket Agent** - LLM-powered requirements extraction (Full-stack)
5. **Design Agent** - LLM-powered design analysis (Full-stack)
6. **Code Agent** - LLM-powered Angular generation (Full-stack)

**Agent orchestration:** Simple sequential chain (Ticket -> Design -> Code). No LangGraph or supervisor patterns needed. Direct chaining with async functions is sufficient and debuggable.

### Critical Pitfalls

1. **Stdout pollution breaks MCP completely** - ALL print/logging must go to stderr. One `print()` corrupts the JSON-RPC stream. Use `print("msg", file=sys.stderr)` and `logging.basicConfig(stream=sys.stderr)`.

2. **Figma rate limits are brutal** - Starter plans: 6 requests/month to non-owned files. Cache ALL responses immediately. Test only on files you own. Have hardcoded fallback JSON for demo.

3. **Jira auth has multiple traps** - SSO never works. Use API tokens from id.atlassian.com. Test auth FIRST before building anything. CAPTCHA triggers after failed attempts.

4. **Azure OpenAI 429 during demo** - Rate limits are per-minute. Implement exponential backoff. Cache LLM responses for demo inputs. Have pre-generated outputs ready.

5. **VS Code MCP config fails silently** - Test with MCP Inspector BEFORE VS Code. Use absolute paths. Fully quit VS Code (Cmd+Q) after config changes. Check Output panel for errors.

## Implications for Roadmap

Based on research, suggested phase structure for 3-4 hour hackathon:

### Phase 1: Foundation and Auth Validation (0:00-0:30)

**Rationale:** Auth failures block everything. Multiple research sources emphasize testing authentication immediately. This phase de-risks the entire hackathon.

**Delivers:**
- Validated API credentials (Jira, Figma, Azure OpenAI)
- Project skeleton with dependencies installed
- Defined interfaces/contracts for all components
- Team ownership assignments

**Addresses:** All table stakes features (foundation for `analyze_ticket`, `analyze_design`, `generate_component`)

**Avoids:** Jira auth traps, Figma rate limit discovery too late, blocked demo due to auth issues

### Phase 2: Parallel Component Build (0:30-2:00)

**Rationale:** With validated auth and defined interfaces, team can work in parallel. This is the main build phase. Architecture research shows HTTP REST enables independent development and testing.

**Delivers:**
- MCP Server with 4 tool stubs (Person 1)
- Jira API client with `fetch_ticket()` (Person 2)
- Figma API client with `fetch_design()` (Person 2)
- Ticket Analyzer Agent (Full-stack)
- Design Analyzer Agent (Full-stack)
- Code Generator Agent (Full-stack)

**Uses:** FastMCP, httpx, Azure OpenAI, FastAPI

**Implements:** Thin MCP Server, Agent Pipeline, Integration Layer

**Avoids:** Git conflicts (one branch per person), stdout pollution (established early), monolithic code

### Phase 3: Integration Checkpoint (2:00-2:30)

**Rationale:** Research emphasizes "integrate at 50%, not at the end." This is the critical checkpoint to force integration and cut scope if needed.

**Delivers:**
- Connected pipeline: MCP -> Backend -> Agents -> APIs
- Happy path working end-to-end
- Scope decisions for remaining time

**Addresses:** `accelerate` tool (the demo money shot)

**Avoids:** Integration never happens, scope creep destroys MVP

### Phase 4: Happy Path Completion (2:30-3:00)

**Rationale:** One working flow beats many broken ones. Focus on polishing the core demo flow rather than adding features.

**Delivers:**
- Complete `accelerate` flow: ticket ID -> generated Angular component
- Cached responses for demo inputs
- Error handling for demo scenarios

**Avoids:** Demo fails from rate limits (cached), half-built features

### Phase 5: Demo Preparation (3:00-3:30)

**Rationale:** Demo-day risks are well-documented: live demo fails, no backup, wrong person presents. This phase mitigates all of them.

**Delivers:**
- Recorded backup video of working demo
- Pre-populated data for demo
- Practiced presentation (3x run-through)
- Best communicator assigned to present

**Avoids:** No backup video, unpracticed demo, wrong presenter

### Phase 6: Demo (3:30-4:00)

**Rationale:** This is what judges see. Everything else is preparation for this moment.

**Delivers:**
- Live demonstration of ticket ID -> generated component
- Answers to anticipated questions

### Phase Ordering Rationale

- **Auth first (Phase 1):** Every downstream phase depends on working API connections. 30 minutes upfront saves hours of debugging later.
- **Parallel build (Phase 2):** HTTP REST architecture enables independent development. Each person owns a complete, testable module.
- **Integration at 50% (Phase 3):** Research unanimously warns against end-of-hackathon integration. Force it at midpoint.
- **Happy path before features (Phase 4):** Table stakes trump differentiators in hackathon context.
- **Demo prep as phase (Phase 5):** Not an afterthought. Dedicated time prevents "still coding 10 minutes before demo."

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2 (Figma Client):** Rate limit workarounds, caching strategy, handling Starter plan restrictions
- **Phase 2 (Code Agent):** Angular-specific generation patterns, workspace pattern extraction

Phases with standard patterns (skip research-phase):
- **Phase 1 (Auth):** Well-documented, standard API token patterns
- **Phase 2 (MCP Server):** FastMCP tutorial is comprehensive, decorator pattern is simple
- **Phase 2 (Jira Client):** REST API v3 is well-documented

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Verified with official MCP SDK docs, PyPI, Azure OpenAI samples |
| Features | HIGH | Based on MCP spec, existing MCP implementations, official Figma/Jira docs |
| Architecture | HIGH | Patterns verified via MCP SDK, FastAPI, established agent patterns |
| Pitfalls | HIGH | Multiple authoritative sources, community experience documented |

**Overall confidence:** HIGH

### Gaps to Address

- **Figma rate limits for demo:** Need to confirm team has Full seat access OR prepare cached responses before hackathon
- **Azure OpenAI quota:** Should request quota increase before hackathon if possible
- **Angular workspace patterns:** Code agent needs examples of existing project patterns for high-quality output
- **VS Code MCP version:** Need to verify VS Code version has MCP support (relatively recent feature)

## Sources

### Primary (HIGH confidence)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Official repository, FastMCP patterns
- [MCP Documentation](https://modelcontextprotocol.io/) - Protocol specification, debugging guide
- [OpenAI Python Library](https://pypi.org/project/openai/) - AzureOpenAI class usage
- [Azure OpenAI Samples](https://learn.microsoft.com/en-us/samples/azure/azure-sdk-for-python/openai-samples/) - Integration patterns
- [Figma REST API](https://developers.figma.com/docs/rest-api/) - API documentation
- [Jira REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/) - API documentation

### Secondary (MEDIUM confidence)
- [Figma MCP Server](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/) - Available tools
- [Atlassian MCP Server](https://github.com/atlassian/atlassian-mcp-server) - Jira integration option
- [Angular CLI MCP Server](https://angular.dev/ai/mcp) - Scaffolding option
- [VS Code MCP Docs](https://code.visualstudio.com/docs/copilot/customization/mcp-servers) - Configuration

### Tertiary (LOW confidence)
- [Figma Rate Limits](https://help.figma.com/hc/en-us/articles/34963238552855-What-if-I-m-rate-limited) - Rate limit details vary by plan
- Community hackathon guides - Demo tips and anti-patterns

---
*Research completed: 2026-01-21*
*Ready for roadmap: yes*
