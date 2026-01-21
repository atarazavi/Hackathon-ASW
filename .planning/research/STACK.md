# Technology Stack

**Project:** Frontend Accelerator MCP Server
**Researched:** 2026-01-21
**Confidence:** HIGH (verified with official documentation and PyPI)

## Executive Recommendation

For a 3-4 hour hackathon building an MCP server with multi-agent orchestration:

**Use vanilla Python with the official MCP SDK + direct Azure OpenAI calls.** Skip heavy agent frameworks - they add complexity without proportional benefit for a hackathon demo.

---

## Recommended Stack

### Core: MCP Server

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| `mcp` | 1.25.0 | MCP server implementation | Official Anthropic SDK. FastMCP decorator pattern is dead simple - tools defined in 3 lines of code. |
| Python | 3.10+ | Runtime | Required by MCP SDK. Use 3.11+ for performance if available. |

**Installation:**
```bash
pip install "mcp[cli]>=1.25,<2"
```

**Why this version:** v1.x is production-stable. v2 is pre-alpha (Q1 2026 release). Pin to `<2` to avoid breaking changes.

### LLM Integration: Azure OpenAI

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| `openai` | 2.15.0 | Azure OpenAI client | Official library with `AzureOpenAI` class. Same API as OpenAI, just different client instantiation. |
| `azure-identity` | latest | Azure auth | For `DefaultAzureCredential` if not using API keys. |

**Installation:**
```bash
pip install openai>=2.15.0 azure-identity
```

**Usage Pattern:**
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview",  # or newer
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

response = client.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),  # deployment name, not model name
    messages=[{"role": "user", "content": "..."}]
)
```

### Agent Orchestration: Vanilla Approach (RECOMMENDED)

| Approach | Why |
|----------|-----|
| **Vanilla Python classes** | For hackathon, you need ~3 specialized agents (Jira reader, Figma reader, Angular generator). Simple classes with `__call__` or `run()` methods are faster to write and debug than learning a framework. |

**Pattern:**
```python
class JiraAgent:
    def __init__(self, llm_client):
        self.client = llm_client
        self.system_prompt = "You extract requirements from Jira tickets..."

    async def run(self, ticket_data: dict) -> dict:
        response = await self.client.chat.completions.create(
            model=DEPLOYMENT,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": json.dumps(ticket_data)}
            ]
        )
        return self._parse_response(response)
```

**Why not a framework?** You have 3-4 hours. Framework learning curve eats 30-60 minutes. Vanilla approach: write your first agent in 10 minutes.

### API Integrations

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| `httpx` | latest | HTTP client | Async-native, cleaner than `requests` for modern Python. Already a dependency of `openai`. |
| `python-dotenv` | latest | Environment config | Load `.env` files for API keys. |

**Installation:**
```bash
pip install httpx python-dotenv
```

### Development Tools

| Technology | Purpose | Why |
|------------|---------|-----|
| `uv` | Package management | 10-100x faster than pip. MCP SDK recommends it. |
| `ruff` | Linting/formatting | Fast, replaces black+flake8+isort. |

**Installation:**
```bash
# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

# Then use uv for package management
uv pip install "mcp[cli]" openai azure-identity httpx python-dotenv
```

---

## Alternatives Considered (and why NOT to use them)

### Agent Frameworks

| Framework | Status | Why NOT for this hackathon |
|-----------|--------|---------------------------|
| **Microsoft Agent Framework** | Beta (1.0.0b260116) | Requires `--pre` flag, Azure-specific auth setup, learning curve. Overkill for 3 agents. |
| **OpenAI Agents SDK** | Stable | Built for OpenAI Responses API. Works with Azure via `set_default_openai_client` but adds abstraction layer you don't need. |
| **PydanticAI** | Stable (1.44.0) | Great framework, but you'd spend 30+ mins learning it vs. 10 mins writing vanilla. Good for post-hackathon refactor. |
| **LangChain/LangGraph** | Stable | Massive abstraction overhead. "Enterprise" complexity for a hackathon demo. |
| **AutoGen** | Stable | Multi-agent conversation focus. Your use case is orchestrated pipeline, not conversation. |

### MCP Alternatives

| Option | Why NOT |
|--------|---------|
| **Third-party MCP implementations** | Official SDK is well-documented and stable. No reason to use alternatives. |
| **Building from scratch** | MCP protocol is non-trivial. SDK handles transport, serialization, tool registration. |

---

## Complete requirements.txt

```txt
# Core MCP
mcp[cli]>=1.25,<2

# Azure OpenAI
openai>=2.15.0
azure-identity

# HTTP client (for Jira/Figma APIs)
httpx

# Environment management
python-dotenv

# Optional: structured outputs
pydantic>=2.0
```

## Complete pyproject.toml (if using uv/poetry)

```toml
[project]
name = "frontend-accelerator-mcp"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "mcp[cli]>=1.25,<2",
    "openai>=2.15.0",
    "azure-identity",
    "httpx",
    "python-dotenv",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "ruff",
    "pytest",
    "pytest-asyncio",
]
```

---

## Quick Start Code Template

### MCP Server with Tools

```python
# server.py
from mcp.server.fastmcp import FastMCP
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize MCP server
mcp = FastMCP("Frontend Accelerator")

# Initialize Azure OpenAI client
llm = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

@mcp.tool()
async def generate_angular_component(
    jira_ticket_id: str,
    figma_frame_url: str
) -> str:
    """
    Generate an Angular component from Jira requirements and Figma design.

    Args:
        jira_ticket_id: The Jira ticket ID (e.g., PROJ-123)
        figma_frame_url: URL to the Figma frame/component

    Returns:
        Generated Angular component code
    """
    # 1. Fetch Jira ticket (your implementation)
    jira_data = await fetch_jira_ticket(jira_ticket_id)

    # 2. Fetch Figma design (your implementation)
    figma_data = await fetch_figma_frame(figma_frame_url)

    # 3. Generate component via LLM
    response = llm.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are an Angular component generator..."},
            {"role": "user", "content": f"Jira: {jira_data}\nFigma: {figma_data}"}
        ]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    mcp.run(transport="stdio")  # VS Code Copilot uses stdio
```

### Running the Server

```bash
# For development/testing
python server.py

# Or with MCP CLI
mcp run server.py
```

### VS Code Copilot Configuration

Add to VS Code settings or `.vscode/mcp.json`:
```json
{
  "mcpServers": {
    "frontend-accelerator": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "AZURE_OPENAI_API_KEY": "...",
        "AZURE_OPENAI_ENDPOINT": "...",
        "AZURE_OPENAI_DEPLOYMENT": "..."
      }
    }
  }
}
```

---

## Environment Variables Required

```bash
# .env file
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o  # or your deployment name
AZURE_OPENAI_API_VERSION=2024-08-01-preview

# Jira
JIRA_BASE_URL=https://your-org.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your-jira-token

# Figma
FIGMA_ACCESS_TOKEN=your-figma-token
```

---

## Post-Hackathon Upgrade Path

If demo succeeds and you want to productionize:

1. **Add PydanticAI** for structured outputs and tool validation
2. **Add Microsoft Agent Framework** if you need complex multi-agent workflows
3. **Add proper error handling** with retries and circuit breakers
4. **Add observability** with OpenTelemetry/Logfire
5. **Switch to HTTP transport** if deploying as a service (vs local stdio)

---

## Sources

- [MCP Python SDK - GitHub](https://github.com/modelcontextprotocol/python-sdk) - Official repository
- [MCP Python SDK - PyPI](https://pypi.org/project/mcp/) - Version 1.25.0
- [MCP Documentation](https://modelcontextprotocol.github.io/python-sdk/) - Official docs
- [OpenAI Python Library - PyPI](https://pypi.org/project/openai/) - Version 2.15.0
- [Azure OpenAI Samples](https://learn.microsoft.com/en-us/samples/azure/azure-sdk-for-python/openai-samples/) - Microsoft Learn
- [Microsoft Agent Framework - GitHub](https://github.com/microsoft/agent-framework) - For future reference
- [PydanticAI - PyPI](https://pypi.org/project/pydantic-ai/) - Version 1.44.0, for future reference
- [FastMCP Tutorial](https://gofastmcp.com/tutorials/create-mcp-server) - Tool definition patterns
- [Azure OpenAI with OpenAI Agents SDK](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/use-azure-openai-and-apim-with-the-openai-agents-sdk/4392537) - Integration pattern
