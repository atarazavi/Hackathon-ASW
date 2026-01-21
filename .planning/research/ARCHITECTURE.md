# Architecture Patterns

**Domain:** Frontend Accelerator (MCP Server + Python Backend + Multi-Agent)
**Researched:** 2026-01-21
**Confidence:** HIGH (patterns verified via official MCP SDK docs and established agent frameworks)

## Executive Summary

For a 3-4 hour hackathon with 6 people working in parallel, the architecture prioritizes:
1. **Clear module boundaries** - Each person owns a complete, testable unit
2. **Simple communication** - HTTP REST between MCP server and Python backend
3. **Sequential agent chain** - Ticket -> Design -> Code, no complex orchestration needed
4. **Minimal framework overhead** - Direct Azure OpenAI calls, not LangChain/LangGraph

## Recommended Architecture

```
+------------------+       HTTP/REST       +------------------+
|   VS Code        | <------------------> |   Python Backend |
|   Copilot        |                      |                  |
+--------+---------+                      +--------+---------+
         |                                         |
         v                                         v
+------------------+                      +------------------+
|   MCP Server     |                      |  Agent Pipeline  |
|   (FastMCP)      |                      |                  |
|                  |                      | Ticket -> Design |
| - analyze_ticket |                      |    -> Code       |
| - analyze_design |                      +--------+---------+
| - generate_code  |                               |
+------------------+                      +--------+---------+
                                          |  External APIs   |
                                          | - Jira Cloud     |
                                          | - Figma          |
                                          | - Azure OpenAI   |
                                          +------------------+
```

## Communication Pattern: HTTP REST (Recommended)

### Why HTTP over Subprocess/stdio

| Criterion | HTTP REST | Subprocess (stdio) |
|-----------|-----------|-------------------|
| **Parallel development** | Backend and MCP server develop independently | Tightly coupled startup |
| **Testing** | Test backend with curl/Postman | Must test through MCP client |
| **Debugging** | Standard HTTP logging | stdio debugging harder |
| **Team boundaries** | Clean separation | Shared process lifecycle |
| **Hackathon fit** | Everyone knows REST | MCP transport details obscure |

**Decision:** Use HTTP REST. MCP server calls Python backend via `httpx.AsyncClient`.

### Implementation Pattern

**MCP Server (TypeScript or Python):**
```python
# mcp_server/main.py
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("FrontendAccelerator")
BACKEND_URL = "http://localhost:8000"

@mcp.tool()
async def analyze_ticket(ticket_id: str) -> dict:
    """Fetch and analyze a Jira ticket, identifying requirements and gaps."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/api/analyze-ticket",
            json={"ticket_id": ticket_id},
            timeout=60.0  # LLM calls can be slow
        )
        return response.json()

@mcp.tool()
async def analyze_design(figma_url: str, ticket_context: dict) -> dict:
    """Analyze a Figma design for component structure and gaps."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/api/analyze-design",
            json={"figma_url": figma_url, "ticket_context": ticket_context},
            timeout=60.0
        )
        return response.json()

@mcp.tool()
async def generate_component(
    ticket_analysis: dict,
    design_analysis: dict,
    workspace_path: str
) -> dict:
    """Generate Angular component matching workspace patterns."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_URL}/api/generate-component",
            json={
                "ticket_analysis": ticket_analysis,
                "design_analysis": design_analysis,
                "workspace_path": workspace_path
            },
            timeout=120.0  # Code generation may take longer
        )
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="stdio")  # VS Code connects via stdio
```

**Python Backend (FastAPI):**
```python
# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TicketRequest(BaseModel):
    ticket_id: str

@app.post("/api/analyze-ticket")
async def analyze_ticket(request: TicketRequest):
    # Call agent pipeline
    from agents.ticket_analyzer import analyze
    return await analyze(request.ticket_id)
```

### Transport Configuration

The MCP server uses **stdio transport** to communicate with VS Code Copilot (this is how VS Code MCP integration works). But internally, the MCP server calls the Python backend over **HTTP**.

```
VS Code <--stdio--> MCP Server <--HTTP--> Python Backend
```

This hybrid approach gives us:
- Standard MCP integration with VS Code (stdio)
- Independent backend development (HTTP)
- Clean team boundaries

## Agent Orchestration: Sequential Chain (Recommended)

### Why Sequential over Complex Patterns

For a hackathon with a clear flow (Ticket -> Design -> Code), sequential chaining is optimal:

| Pattern | Complexity | Debugging | Team Fit |
|---------|------------|-----------|----------|
| **Sequential Chain** | Low | Easy - follow the path | Each agent is isolated |
| LangGraph State Machine | High | Requires graph tracing | Shared state complexity |
| Parallel Fan-out | Medium | Race conditions | Coordination overhead |
| Supervisor/Router | Medium | Routing logic to debug | Central bottleneck |

**Decision:** Simple sequential chain. No framework needed.

### Implementation Pattern

**Option A: Direct Chaining (Recommended for Hackathon)**
```python
# backend/pipeline.py
async def run_pipeline(ticket_id: str, figma_url: str, workspace_path: str):
    """Sequential pipeline: Ticket -> Design -> Code"""

    # Step 1: Analyze ticket
    ticket_result = await ticket_agent.analyze(ticket_id)

    # Step 2: Analyze design (uses ticket context)
    design_result = await design_agent.analyze(
        figma_url=figma_url,
        ticket_context=ticket_result
    )

    # Step 3: Generate code (uses both)
    code_result = await code_agent.generate(
        ticket_analysis=ticket_result,
        design_analysis=design_result,
        workspace_path=workspace_path
    )

    return {
        "ticket_analysis": ticket_result,
        "design_analysis": design_result,
        "generated_code": code_result
    }
```

**Option B: With Microsoft Agent Framework (if team knows it)**
```python
# backend/pipeline.py
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIResponsesClient

client = AzureOpenAIResponsesClient(
    endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_KEY"]
)

ticket_agent = ChatAgent(
    client=client,
    model="gpt-4o",
    instructions="You analyze Jira tickets..."
)
```

**Recommendation:** Use Option A (direct Azure OpenAI calls via `openai` SDK). Frameworks add complexity and learning curve that don't fit a 3-4 hour hackathon.

### Agent-to-Agent Data Flow

```
TicketAgent                  DesignAgent                  CodeAgent
    |                            |                            |
    | ticket_analysis            |                            |
    |--------------------------->|                            |
    |                            | design_analysis            |
    |                            |--------------------------->|
    |                            |                            |
    |<--------------------------------------------------------|
    |              final_result (all three outputs)           |
```

Each agent receives:
- Its specific input (ticket_id, figma_url, workspace_path)
- Context from previous agents (accumulated in pipeline)

## Component Boundaries (For Parallel Development)

### Directory Structure

```
asw-frontend-accelerator/
├── mcp-server/                 # Person 1: MCP Server
│   ├── pyproject.toml
│   ├── src/
│   │   └── mcp_server/
│   │       ├── __init__.py
│   │       ├── main.py         # FastMCP entry point
│   │       └── tools.py        # Tool definitions
│   └── tests/
│
├── backend/                    # Person 2: Backend Lead
│   ├── pyproject.toml
│   ├── src/
│   │   └── backend/
│   │       ├── __init__.py
│   │       ├── main.py         # FastAPI app
│   │       ├── config.py       # Azure OpenAI, API keys
│   │       ├── pipeline.py     # Agent orchestration
│   │       └── agents/         # Agent implementations
│   │           ├── __init__.py
│   │           ├── base.py     # Base agent class
│   │           ├── ticket.py   # Person 3: Ticket agent
│   │           ├── design.py   # Person 4: Design agent
│   │           └── code.py     # Person 5: Code agent
│   └── tests/
│
├── integrations/               # Person 3: Integrations
│   ├── pyproject.toml
│   ├── src/
│   │   └── integrations/
│   │       ├── __init__.py
│   │       ├── jira.py         # Jira API client
│   │       └── figma.py        # Figma API client
│   └── tests/
│
├── guidelines/                 # Designers: Content
│   └── design-guidelines.md
│
└── demo/                       # BA: Test data
    ├── sample-tickets/
    └── test-scenarios.md
```

### Team Ownership Map

| Person | Module | Interface | Can Test Independently |
|--------|--------|-----------|------------------------|
| Frontend 1 | `mcp-server/` | HTTP calls to backend | Yes - mock backend responses |
| Full-stack | `backend/` (orchestration) | Imports from `agents/` and `integrations/` | Yes - mock agents |
| Frontend 2 | `integrations/` | Export functions like `fetch_ticket()` | Yes - mock API responses |
| Full-stack | `backend/agents/ticket.py` | Takes ticket data, returns analysis | Yes - mock LLM |
| Full-stack | `backend/agents/design.py` | Takes Figma data, returns analysis | Yes - mock LLM |
| Full-stack | `backend/agents/code.py` | Takes analyses, returns code | Yes - mock LLM |

### Interface Contracts

**Integration -> Agent Interface:**
```python
# integrations/jira.py
async def fetch_ticket(ticket_id: str) -> JiraTicket:
    """
    Returns:
        JiraTicket with fields:
        - id: str
        - summary: str
        - description: str
        - acceptance_criteria: list[str]
        - linked_designs: list[str]  # Figma URLs if any
    """
```

**Agent -> Pipeline Interface:**
```python
# agents/base.py
class AgentResult(BaseModel):
    success: bool
    data: dict
    errors: list[str] = []

# agents/ticket.py
async def analyze(ticket_id: str) -> AgentResult:
    """
    Returns AgentResult with data containing:
    - requirements: list[str]
    - acceptance_criteria: list[str]
    - missing_info: list[str]
    - linked_figma_urls: list[str]
    """
```

**MCP -> Backend Interface:**
```python
# Each MCP tool maps to one backend endpoint
POST /api/analyze-ticket    -> ticket agent
POST /api/analyze-design    -> design agent
POST /api/generate-component -> code agent
POST /api/run-pipeline      -> full chain (optional)
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         VS Code Copilot                         │
│                                                                 │
│  User: "Analyze ticket PROJ-123 and generate a component"       │
└─────────────────────────┬───────────────────────────────────────┘
                          │ stdio (JSON-RPC)
                          v
┌─────────────────────────────────────────────────────────────────┐
│                        MCP Server                               │
│                                                                 │
│  Tool: analyze_ticket(ticket_id="PROJ-123")                     │
│  Tool: analyze_design(figma_url="...", ticket_context={...})    │
│  Tool: generate_component(...)                                  │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP POST
                          v
┌─────────────────────────────────────────────────────────────────┐
│                      Python Backend (FastAPI)                   │
│                                                                 │
│  POST /api/analyze-ticket                                       │
│    │                                                            │
│    ├──> Jira Client ──> Jira Cloud API ──> ticket data         │
│    │                                                            │
│    └──> Ticket Agent ──> Azure OpenAI ──> analysis             │
│                                                                 │
│  POST /api/analyze-design                                       │
│    │                                                            │
│    ├──> Figma Client ──> Figma API ──> design data             │
│    │                                                            │
│    └──> Design Agent ──> Azure OpenAI ──> analysis             │
│                                                                 │
│  POST /api/generate-component                                   │
│    │                                                            │
│    ├──> Workspace Scanner ──> local files ──> patterns         │
│    │                                                            │
│    └──> Code Agent ──> Azure OpenAI ──> Angular component      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Patterns to Follow

### Pattern 1: Thin MCP Server

**What:** MCP server contains no business logic. It only:
- Defines tool schemas
- Calls backend HTTP endpoints
- Returns responses

**Why:**
- MCP server is hard to test (requires MCP client)
- Business logic in Python backend is easy to test
- Clear ownership boundary

**Example:**
```python
# Good: MCP tool is just an HTTP wrapper
@mcp.tool()
async def analyze_ticket(ticket_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BACKEND}/api/analyze-ticket", json={"ticket_id": ticket_id})
        return response.json()

# Bad: Business logic in MCP tool
@mcp.tool()
async def analyze_ticket(ticket_id: str) -> dict:
    ticket = await jira.fetch(ticket_id)  # Don't do this
    analysis = await llm.analyze(ticket)   # Don't do this
    return analysis
```

### Pattern 2: Agent as Pure Function

**What:** Each agent is a stateless async function that:
- Takes structured input
- Calls LLM with prompt + input
- Returns structured output

**Why:**
- Easy to test (mock LLM response)
- Easy to develop in parallel (no shared state)
- Easy to debug (input -> output)

**Example:**
```python
# agents/ticket.py
from openai import AsyncAzureOpenAI

client = AsyncAzureOpenAI(...)

async def analyze(ticket_data: JiraTicket) -> AgentResult:
    prompt = f"""Analyze this Jira ticket and extract:
    - Key requirements
    - Acceptance criteria
    - Missing information

    Ticket: {ticket_data.model_dump_json()}
    """

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return AgentResult(
        success=True,
        data=json.loads(response.choices[0].message.content)
    )
```

### Pattern 3: Structured LLM Outputs

**What:** Always request JSON output from LLM with defined schema.

**Why:**
- Predictable downstream processing
- Easier agent chaining (next agent knows what to expect)
- Cleaner error handling

**Example:**
```python
# Use Pydantic models for both input and output
class TicketAnalysis(BaseModel):
    requirements: list[str]
    acceptance_criteria: list[str]
    missing_info: list[str]
    complexity: Literal["low", "medium", "high"]

# Request structured output
response = await client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    response_format={"type": "json_object"}  # Or use function calling
)
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Framework Overhead

**What:** Using LangChain/LangGraph for simple sequential chains.

**Why bad:**
- Learning curve eats hackathon time
- Debugging through framework abstractions is slow
- Overkill for 3-4 agents in a line

**Instead:** Direct Azure OpenAI SDK calls with simple async functions.

### Anti-Pattern 2: Shared Mutable State

**What:** Agents reading/writing to shared state object.

**Why bad:**
- Race conditions in parallel development
- Hard to test individual agents
- State bugs are hard to track

**Instead:** Each agent receives input, returns output. Pipeline manages data flow.

### Anti-Pattern 3: Monolithic Backend

**What:** All agent logic in one file.

**Why bad:**
- Merge conflicts when 3 people edit same file
- Can't test agents independently
- Hard to see what each person owns

**Instead:** One file per agent, clear import boundaries.

### Anti-Pattern 4: Complex Orchestration

**What:** Building supervisor agents, routers, or parallel execution for MVP.

**Why bad:**
- "Debugging graph-based orchestration is hard" - multiple sources agree
- Hackathon time is precious
- Sequential flow is sufficient for demo

**Instead:** Start with simple sequential chain. Add complexity only if needed.

## Scalability Considerations

| Concern | Hackathon (Day 1) | Post-Hackathon | Production |
|---------|-------------------|----------------|------------|
| Concurrent users | Single user demo | Add request queuing | Load balancer + workers |
| Agent parallelism | Sequential only | Parallel where independent | LangGraph or similar |
| LLM latency | Accept 10-30s | Add streaming | Async job queue |
| Error handling | Log and return error | Retry logic | Circuit breakers |

For hackathon: Don't optimize prematurely. Get the flow working first.

## Quick Reference: Who Builds What

| Component | Owner | Depends On | Delivers |
|-----------|-------|------------|----------|
| MCP Server | Frontend 1 | Backend running | `mcp-server/` working with VS Code |
| Backend API | Full-stack | Agents, Integrations | FastAPI with endpoints |
| Jira Client | Frontend 2 | Jira API key | `integrations/jira.py` |
| Figma Client | Frontend 2 | Figma API key | `integrations/figma.py` |
| Ticket Agent | Full-stack | Azure OpenAI | `agents/ticket.py` |
| Design Agent | Full-stack | Azure OpenAI | `agents/design.py` |
| Code Agent | Full-stack | Azure OpenAI | `agents/code.py` |
| Guidelines | Designers | None | `guidelines/design-guidelines.md` |
| Test Data | BA | Jira, Figma | Sample tickets, scenarios |

## Sources

**MCP Communication Patterns:**
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Official SDK with transport options
- [FastMCP](https://github.com/jlowin/fastmcp) - Simplified MCP server framework
- [MCP Architecture Specification](https://modelcontextprotocol.io/specification/2025-06-18/architecture) - Official architecture docs
- [From stdio to HTTP SSE](https://apisix.org/blog/2025/04/21/host-mcp-server-with-api-gateway/) - Transport comparison

**Agent Orchestration:**
- [LangChain Multi-Agent Docs](https://docs.langchain.com/oss/python/langchain/multi-agent) - Multi-agent patterns
- [Choosing the Right Multi-Agent Architecture](https://www.blog.langchain.com/choosing-the-right-multi-agent-architecture/) - Pattern comparison
- [Google's Multi-Agent Design Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) - Eight foundational patterns
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) - Unified SK + AutoGen

**Azure OpenAI Integration:**
- [Azure OpenAI Function Calling](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/function-calling) - Tool calling patterns
- [OpenAI Agents SDK with Azure](https://learn.microsoft.com/en-us/answers/questions/2239161/is-the-new-openai-agents-sdk-for-python-supported) - SDK compatibility

**REST API to MCP Patterns:**
- [FastMCP REST API Tutorial](https://gofastmcp.com/tutorials/rest-api) - HTTP client patterns
- [From REST API to MCP Server](https://www.stainless.com/mcp/from-rest-api-to-mcp-server) - Conversion patterns
