# Phase 2A: Backend - Research

**Researched:** 2026-01-21
**Domain:** FastAPI + Azure OpenAI + Design Analysis Agent
**Confidence:** HIGH

## Summary

This phase builds a Python FastAPI backend with a `/analyze` endpoint that uses Azure OpenAI to analyze Figma design data for completeness issues. The backend receives JSON design data from the Figma plugin, passes it to an LLM agent with guidelines context, and returns structured findings with severity levels and recommendations.

The core technical challenges are:
1. Async Azure OpenAI integration with structured JSON outputs
2. Pydantic models for request/response validation
3. Prompt engineering for reliable design analysis across four categories

**Primary recommendation:** Use `AsyncAzureOpenAI` with `beta.chat.completions.parse()` for structured outputs via Pydantic models. Keep the agent as a single async function with a comprehensive prompt, not a complex multi-agent system. Cache the client at app startup via FastAPI lifespan.

## Standard Stack

The existing backend already has the required dependencies. No new packages needed.

### Core (Already Installed)

| Library | Version | Purpose | Already in requirements.txt |
|---------|---------|---------|----------------------------|
| `fastapi` | >=0.109.0 | Web framework | Yes |
| `uvicorn` | >=0.27.0 | ASGI server | Yes |
| `openai` | >=1.12.0 | Azure OpenAI SDK with `AsyncAzureOpenAI` | Yes |
| `pydantic-settings` | >=2.1.0 | Type-safe config from `.env` | Yes |
| `python-dotenv` | >=1.0.0 | Load `.env` files | Yes |

### Implicit Dependencies (via openai)

| Library | Purpose |
|---------|---------|
| `httpx` | Async HTTP client (used by openai SDK) |
| `pydantic` | Data validation (v2 comes with fastapi) |

### Not Needed

| Library | Why Not |
|---------|---------|
| `instructor` | Adds abstraction over native structured outputs, not needed for single agent |
| `langchain` / `pydanticai` | Overkill for hackathon, direct SDK is simpler |
| `aiohttp` | httpx is already bundled with openai |

**No installation needed - existing requirements.txt is sufficient.**

## Architecture Patterns

### Recommended Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with lifespan
│   ├── config.py            # Pydantic Settings (exists)
│   ├── routers/
│   │   ├── __init__.py
│   │   └── review.py        # /analyze endpoint
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request.py       # DesignData, Frame models
│   │   └── response.py      # Finding, AnalysisResponse models
│   └── services/
│       ├── __init__.py
│       └── analyzer.py      # Azure OpenAI analysis logic
├── guidelines/
│   └── GUIDELINES.md        # Design guidelines for agent (Phase 2C)
├── requirements.txt         # (exists)
└── .env                     # (exists)
```

### Pattern 1: Lifespan Client Management

**What:** Initialize `AsyncAzureOpenAI` client once at startup, share across requests.
**When to use:** Always - avoid creating client per request.

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from openai import AsyncAzureOpenAI
from .config import Settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create async client
    settings = Settings()
    app.state.openai_client = AsyncAzureOpenAI(
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
    )
    app.state.settings = settings
    yield
    # Shutdown: client closes automatically

app = FastAPI(title="Design Review API", lifespan=lifespan)
```

### Pattern 2: Structured Outputs with Pydantic

**What:** Use `beta.chat.completions.parse()` with Pydantic model as `response_format`.
**When to use:** When you need guaranteed JSON structure from LLM.

```python
# app/models/response.py
from pydantic import BaseModel
from typing import Literal
from enum import Enum

class Severity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

class FindingCategory(str, Enum):
    MISSING_STATES = "missing_states"
    ACCESSIBILITY = "accessibility"
    DESIGN_SYSTEM = "design_system"
    RESPONSIVENESS = "responsiveness"

class Finding(BaseModel):
    category: FindingCategory
    severity: Severity
    title: str
    description: str
    recommendation: str
    affected_frames: list[str]

class AnalysisResult(BaseModel):
    findings: list[Finding]
    summary: str
    frames_analyzed: int

# Usage in service
completion = await client.beta.chat.completions.parse(
    model=deployment_name,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    response_format=AnalysisResult,
)
result = completion.choices[0].message.parsed  # Already typed!
```

### Pattern 3: Request Model with Nested Frames

**What:** Define Pydantic models that mirror Figma plugin's JSON structure.
**When to use:** For the `/analyze` endpoint request body.

```python
# app/models/request.py
from pydantic import BaseModel

class TextNode(BaseModel):
    content: str
    font_size: float | None = None
    font_weight: str | None = None
    fill_color: str | None = None  # hex color

class FrameLayer(BaseModel):
    id: str
    name: str
    type: str  # "TEXT", "FRAME", "RECTANGLE", etc.
    visible: bool = True
    children: list["FrameLayer"] = []
    text: TextNode | None = None
    fill_color: str | None = None
    background_color: str | None = None

class Frame(BaseModel):
    id: str
    name: str
    width: float
    height: float
    layers: list[FrameLayer]

class DesignDataRequest(BaseModel):
    frames: list[Frame]
    guidelines: str | None = None  # Optional override
```

### Pattern 4: Async Endpoint with Dependency Injection

**What:** Use FastAPI's `Request` object to access shared state.
**When to use:** For accessing the OpenAI client in endpoints.

```python
# app/routers/review.py
from fastapi import APIRouter, Request
from ..models.request import DesignDataRequest
from ..models.response import AnalysisResult
from ..services.analyzer import analyze_design

router = APIRouter(prefix="/review", tags=["review"])

@router.post("/analyze", response_model=AnalysisResult)
async def analyze(request: Request, data: DesignDataRequest) -> AnalysisResult:
    client = request.app.state.openai_client
    settings = request.app.state.settings

    result = await analyze_design(
        client=client,
        deployment=settings.azure_openai_deployment,
        design_data=data,
    )
    return result
```

### Anti-Patterns to Avoid

- **Creating client per request:** Wastes resources, use lifespan instead
- **Sync client in async endpoint:** Blocks event loop, use `AsyncAzureOpenAI`
- **Complex multi-agent orchestration:** Overkill for hackathon, single prompt is sufficient
- **Returning raw LLM text:** Always use structured outputs for predictable downstream parsing
- **Hardcoding guidelines in code:** Load from file so designers can update without code changes

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| JSON output parsing | Regex/string parsing of LLM response | `beta.chat.completions.parse()` | Structured outputs guarantee valid JSON |
| Request validation | Manual JSON parsing | Pydantic models | Auto-validation, error messages, OpenAPI docs |
| Async HTTP client | `requests` with threads | `AsyncAzureOpenAI` (uses httpx) | Native async, connection pooling |
| Config management | `os.environ` everywhere | Pydantic Settings | Type-safe, validation, `.env` support |
| Error responses | Manual JSON error building | FastAPI's HTTPException | Consistent error format |

**Key insight:** The openai SDK's structured outputs feature eliminates the biggest pain point (parsing LLM responses). Don't fight it with custom JSON extraction.

## Common Pitfalls

### Pitfall 1: Using Wrong API Version for Structured Outputs

**What goes wrong:** `response_format` with Pydantic model returns error or is ignored.
**Why it happens:** Structured outputs require API version `2024-08-01-preview` or later.
**How to avoid:** Update `.env` to use `AZURE_OPENAI_API_VERSION=2024-10-01-preview` or later.
**Warning signs:** Error mentioning "response_format" or "structured outputs not supported".

### Pitfall 2: Model Doesn't Support Structured Outputs

**What goes wrong:** `beta.chat.completions.parse()` fails or returns unstructured text.
**Why it happens:** Only certain models support structured outputs: gpt-4o (2024-08-06+), gpt-4o-mini.
**How to avoid:** Verify deployment uses supported model version.
**Warning signs:** Error about "json_schema" or model returning prose instead of JSON.

### Pitfall 3: Pydantic Model Too Complex for OpenAI

**What goes wrong:** "Invalid schema for response_format" error.
**Why it happens:** OpenAI's JSON Schema support is stricter than Pydantic's full capabilities.
**How to avoid:** Keep models simple - use basic types, avoid `Optional` (use `| None`), avoid complex validators.
**Warning signs:** Cryptic schema validation errors on otherwise valid Pydantic models.

### Pitfall 4: Blocking Event Loop with Sync Client

**What goes wrong:** Endpoint hangs or times out under load.
**Why it happens:** Using `AzureOpenAI` (sync) instead of `AsyncAzureOpenAI` in async endpoint.
**How to avoid:** Always use `AsyncAzureOpenAI` and `await` all calls.
**Warning signs:** High latency, poor concurrency, uvicorn worker exhaustion.

### Pitfall 5: Azure OpenAI 429 Rate Limits

**What goes wrong:** Intermittent failures during demo, "Too Many Requests" errors.
**Why it happens:** Azure OpenAI has strict per-minute rate limits.
**How to avoid:**
- Add retry logic with exponential backoff
- Cache responses for demo inputs
- Have pre-generated fallback response ready
**Warning signs:** Works in testing, fails during rapid demo iterations.

### Pitfall 6: Guidelines File Not Found

**What goes wrong:** `FileNotFoundError` when loading guidelines.
**Why it happens:** Working directory differs between dev and production.
**How to avoid:** Use absolute paths relative to the file, not working directory.
**Warning signs:** Works locally, fails in deployment or different launch context.

```python
# WRONG
with open("guidelines/GUIDELINES.md") as f:
    guidelines = f.read()

# RIGHT
from pathlib import Path
GUIDELINES_PATH = Path(__file__).parent.parent / "guidelines" / "GUIDELINES.md"
with open(GUIDELINES_PATH) as f:
    guidelines = f.read()
```

## Code Examples

### Complete Analyzer Service

```python
# app/services/analyzer.py
from pathlib import Path
from openai import AsyncAzureOpenAI
from ..models.request import DesignDataRequest
from ..models.response import AnalysisResult

GUIDELINES_PATH = Path(__file__).parent.parent.parent / "guidelines" / "GUIDELINES.md"

SYSTEM_PROMPT = """You are a design review expert. Analyze the provided Figma design data and identify issues in four categories:

1. MISSING_STATES: Missing UI states (loading, error, empty, disabled, hover, focus, pressed)
2. ACCESSIBILITY: Accessibility gaps (contrast issues, missing labels, focus states, touch targets)
3. DESIGN_SYSTEM: Design system violations (inconsistent spacing, colors not matching tokens, typography mismatches)
4. RESPONSIVENESS: Responsiveness gaps (missing breakpoints when multiple frame sizes suggest responsive design)

For each finding:
- Assign severity: "critical" (blocks users), "warning" (degrades UX), "info" (nice to fix)
- Provide a clear title
- Describe what's wrong
- Give an actionable recommendation
- List which frames are affected

Use the guidelines document for reference on expected standards.

Respond with a JSON object containing:
- findings: array of issues found
- summary: brief overall assessment
- frames_analyzed: count of frames reviewed
"""

async def analyze_design(
    client: AsyncAzureOpenAI,
    deployment: str,
    design_data: DesignDataRequest,
) -> AnalysisResult:
    # Load guidelines
    guidelines = ""
    if GUIDELINES_PATH.exists():
        guidelines = GUIDELINES_PATH.read_text()

    # Override with request guidelines if provided
    if design_data.guidelines:
        guidelines = design_data.guidelines

    # Build user prompt
    user_prompt = f"""## Design Guidelines
{guidelines}

## Design Data to Analyze
{design_data.model_dump_json(indent=2)}

Analyze this design data and return structured findings."""

    completion = await client.beta.chat.completions.parse(
        model=deployment,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format=AnalysisResult,
        temperature=0.2,  # Lower for more consistent analysis
    )

    return completion.choices[0].message.parsed
```

### Complete Router with Error Handling

```python
# app/routers/review.py
from fastapi import APIRouter, Request, HTTPException
from openai import APIError, RateLimitError
from ..models.request import DesignDataRequest
from ..models.response import AnalysisResult
from ..services.analyzer import analyze_design

router = APIRouter(prefix="/review", tags=["review"])

@router.post("/analyze", response_model=AnalysisResult)
async def analyze(request: Request, data: DesignDataRequest) -> AnalysisResult:
    """
    Analyze design data for completeness issues.

    Checks for:
    - Missing UI states (loading, error, empty, etc.)
    - Accessibility gaps (contrast, labels, focus)
    - Design system violations (spacing, colors, typography)
    - Responsiveness gaps (missing breakpoints)
    """
    client = request.app.state.openai_client
    settings = request.app.state.settings

    try:
        result = await analyze_design(
            client=client,
            deployment=settings.azure_openai_deployment,
            design_data=data,
        )
        return result
    except RateLimitError as e:
        raise HTTPException(
            status_code=429,
            detail="Azure OpenAI rate limit exceeded. Please try again shortly.",
        )
    except APIError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Azure OpenAI error: {str(e)}",
        )
```

### Updated Main with Lifespan and Router

```python
# app/main.py
from contextlib import asynccontextmanager
from functools import lru_cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncAzureOpenAI
from .config import Settings
from .routers import review

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    app.state.openai_client = AsyncAzureOpenAI(
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
    )
    app.state.settings = settings
    yield

app = FastAPI(title="Design Review API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Required for Figma plugin null origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(review.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

## Prompt Engineering for Design Analysis

### Four Analysis Categories

Each category maps to a specific requirement:

| Category | Requirement | What to Check |
|----------|-------------|---------------|
| `MISSING_STATES` | AGENT-01 | loading, error, empty, disabled, hover, focus, pressed states |
| `ACCESSIBILITY` | AGENT-02 | contrast ratios, labels, focus indicators, touch target sizes |
| `DESIGN_SYSTEM` | AGENT-03 | spacing consistency, color token usage, typography scale |
| `RESPONSIVENESS` | AGENT-04 | breakpoint coverage when multiple frame widths exist |

### Prompt Tips

1. **Be specific about state names:** Enumerate exactly which states to look for
2. **Provide guidelines context:** Include the guidelines document in the prompt
3. **Request structured output:** Use Pydantic model to guarantee format
4. **Set low temperature (0.1-0.3):** For consistent analysis across runs
5. **Include frame names:** So findings reference specific artboards

### Handling Multiple Frames for Responsiveness

When comparing frames for responsive design gaps:

```python
# In analyzer service, add logic to detect responsive intent
def detect_responsive_intent(frames: list[Frame]) -> bool:
    """Check if frames suggest responsive design (similar names, different widths)."""
    widths = {f.width for f in frames}
    return len(widths) > 1  # Multiple unique widths suggest breakpoints
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `response_format={"type": "json_object"}` | `response_format=PydanticModel` | OpenAI SDK 1.42+ (Aug 2024) | Guaranteed schema compliance |
| Sync `AzureOpenAI` in async app | `AsyncAzureOpenAI` | Always available | Non-blocking, better concurrency |
| Manual JSON Schema writing | Pydantic model auto-conversion | OpenAI SDK 1.42+ | Less error-prone |
| App globals for client | Lifespan context manager | FastAPI 0.109+ (Jan 2024) | Proper resource management |

**Current best practice:** Use `beta.chat.completions.parse()` with Pydantic models for all structured LLM outputs. This is the "structured outputs" feature that guarantees 100% schema compliance.

## Open Questions

### 1. Guidelines Format

**What we know:** Agent needs guidelines document for reference (AGENT-05).
**What's unclear:** Optimal format for guidelines - prose vs structured checklist.
**Recommendation:** Start with markdown prose, iterate based on LLM performance. The GUIDELINES.md will be created in Phase 2C.

### 2. Frame Data Depth

**What we know:** Plugin will extract layers, styles, tokens from frames.
**What's unclear:** How deep to extract nested children, what properties are most useful.
**Recommendation:** Start with top-level properties and 2 levels of children. Add depth if analysis is missing context.

### 3. Responsiveness Detection Heuristics

**What we know:** AGENT-04 requires detecting missing breakpoints.
**What's unclear:** Best heuristics for determining if frames are meant to be responsive versions.
**Recommendation:** Compare frame names (look for "mobile", "tablet", "desktop" patterns) and widths (320, 768, 1024, 1440 breakpoints).

## Sources

### Primary (HIGH confidence)
- [Azure OpenAI Structured Outputs](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/structured-outputs) - Official Microsoft docs on `beta.chat.completions.parse()`
- [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/) - Official FastAPI docs on Pydantic request models
- [FastAPI Response Model](https://fastapi.tiangolo.com/tutorial/response-model/) - Official FastAPI docs on response serialization
- [OpenAI Python SDK](https://github.com/openai/openai-python) - Official SDK with `AsyncAzureOpenAI` examples

### Secondary (MEDIUM confidence)
- [FastAPI Production Patterns 2025](https://orchestrator.dev/blog/2025-1-30-fastapi-production-patterns/) - Lifespan client management pattern
- [Azure OpenAI Async Streaming FastAPI](https://medium.com/codex/harness-the-power-of-async-streaming-with-azure-openai-and-python-fastapi-1cff7551a72a) - Async integration patterns
- [Instructor Azure Integration](https://python.useinstructor.com/integrations/azure/) - Structured output patterns (using instructor library)
- [OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs) - Official OpenAI guide

### Tertiary (LOW confidence)
- [UI States Article (Trendyol)](https://medium.com/trendyol-tech/simple-ui-problem-states-loading-error-empty-and-content-cbf924b39fcb) - Missing states enumeration
- [WebAIM Contrast](https://webaim.org/resources/contrastchecker/) - WCAG contrast requirements reference

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - existing requirements.txt already has all needed deps
- Architecture: HIGH - patterns verified with official FastAPI and OpenAI docs
- Pitfalls: HIGH - common Azure OpenAI issues well-documented
- Prompt engineering: MEDIUM - design analysis is novel domain, will need iteration

**Research date:** 2026-01-21
**Valid until:** 2026-02-21 (30 days - stable domain)
