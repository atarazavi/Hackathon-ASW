---
phase: 2A-backend
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - backend/app/models/__init__.py
  - backend/app/models/request.py
  - backend/app/models/response.py
  - backend/app/main.py
  - backend/app/routers/review.py
autonomous: true

must_haves:
  truths:
    - "POST /review/analyze endpoint accepts JSON design data"
    - "Endpoint validates request against Pydantic model"
    - "Response follows structured Finding model with severity and category"
    - "AsyncAzureOpenAI client initializes at app startup"
  artifacts:
    - path: "backend/app/models/request.py"
      provides: "DesignDataRequest, Frame, FrameLayer Pydantic models"
      exports: ["DesignDataRequest", "Frame", "FrameLayer", "TextNode"]
    - path: "backend/app/models/response.py"
      provides: "AnalysisResult, Finding models with enums"
      exports: ["AnalysisResult", "Finding", "Severity", "FindingCategory"]
    - path: "backend/app/main.py"
      provides: "FastAPI app with lifespan and router"
      contains: "lifespan"
    - path: "backend/app/routers/review.py"
      provides: "/analyze POST endpoint"
      contains: "@router.post"
  key_links:
    - from: "backend/app/routers/review.py"
      to: "backend/app/models/request.py"
      via: "import DesignDataRequest"
      pattern: "from.*models.request import"
    - from: "backend/app/routers/review.py"
      to: "backend/app/models/response.py"
      via: "import AnalysisResult"
      pattern: "from.*models.response import"
    - from: "backend/app/main.py"
      to: "backend/app/routers/review.py"
      via: "app.include_router"
      pattern: "include_router.*review"
---

<objective>
Create Pydantic request/response models and wire up the /analyze endpoint with AsyncAzureOpenAI client lifecycle.

Purpose: Establish the API contract and async client infrastructure that the analyzer service will use.
Output: Working endpoint skeleton that accepts design data, validates it, and returns a stub response (real analysis in Plan 02).
</objective>

<execution_context>
@~/.claude/get-shit-done/workflows/execute-plan.md
@~/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/2A-backend/2A-RESEARCH.md

# Existing backend files to modify
@backend/app/main.py
@backend/app/config.py
@backend/app/routers/review.py
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create Pydantic models for request and response</name>
  <files>
    backend/app/models/__init__.py
    backend/app/models/request.py
    backend/app/models/response.py
  </files>
  <action>
Create models directory and Pydantic models matching the research patterns:

**backend/app/models/__init__.py:**
```python
from .request import DesignDataRequest, Frame, FrameLayer, TextNode
from .response import AnalysisResult, Finding, Severity, FindingCategory

__all__ = [
    "DesignDataRequest", "Frame", "FrameLayer", "TextNode",
    "AnalysisResult", "Finding", "Severity", "FindingCategory",
]
```

**backend/app/models/request.py:**
- `TextNode`: content, font_size, font_weight, fill_color (all optional except content)
- `FrameLayer`: id, name, type, visible, children (recursive), text, fill_color, background_color
- `Frame`: id, name, width, height, layers (list of FrameLayer)
- `DesignDataRequest`: frames (list of Frame), guidelines (optional string override)

**backend/app/models/response.py:**
- `Severity` enum: CRITICAL, WARNING, INFO (str values for JSON)
- `FindingCategory` enum: MISSING_STATES, ACCESSIBILITY, DESIGN_SYSTEM, RESPONSIVENESS
- `Finding`: category, severity, title, description, recommendation, affected_frames (list of str)
- `AnalysisResult`: findings (list of Finding), summary (str), frames_analyzed (int)

Use `str, Enum` pattern for enums so they serialize as strings. Use `| None` for optional fields (not Optional - cleaner for OpenAI structured outputs).
  </action>
  <verify>
```bash
cd /Users/chatdna/asw-frontend-accelerator/backend
python -c "from app.models import DesignDataRequest, AnalysisResult, Finding, Severity, FindingCategory; print('Models import OK')"
```
  </verify>
  <done>Models importable, enums serialize as strings, recursive FrameLayer works</done>
</task>

<task type="auto">
  <name>Task 2: Update main.py with lifespan and wire endpoint</name>
  <files>
    backend/app/main.py
    backend/app/routers/review.py
  </files>
  <action>
**Update backend/app/main.py:**

1. Add `asynccontextmanager` import from contextlib
2. Add `AsyncAzureOpenAI` import from openai
3. Create lifespan context manager that:
   - Creates Settings instance
   - Creates AsyncAzureOpenAI client with settings values
   - Stores both on `app.state.openai_client` and `app.state.settings`
   - Yields (no shutdown cleanup needed - client auto-closes)
4. Pass `lifespan=lifespan` to FastAPI constructor
5. Import and include the review router: `app.include_router(review.router)`
6. Remove the `get_settings()` function with `@lru_cache` (no longer needed - settings on app.state)

**Update backend/app/routers/review.py:**

1. Import Request from fastapi
2. Import HTTPException from fastapi
3. Import DesignDataRequest from `..models.request`
4. Import AnalysisResult, Finding, Severity, FindingCategory from `..models.response`
5. Create stub endpoint:
```python
@router.post("/analyze", response_model=AnalysisResult)
async def analyze(request: Request, data: DesignDataRequest) -> AnalysisResult:
    """
    Analyze design data for completeness issues.

    Stub implementation - returns empty findings.
    Real analysis added in Plan 02.
    """
    # Access client (will be used in Plan 02)
    client = request.app.state.openai_client
    settings = request.app.state.settings

    # Return stub response for now
    return AnalysisResult(
        findings=[],
        summary="Analysis pending - stub response",
        frames_analyzed=len(data.frames),
    )
```

IMPORTANT: Update the API version in config.py from "2024-02-15-preview" to "2024-10-01-preview" for structured outputs support.
  </action>
  <verify>
```bash
cd /Users/chatdna/asw-frontend-accelerator/backend

# Check syntax
python -c "from app.main import app; print('App imports OK')"

# Start server briefly and test endpoint
timeout 5 uvicorn app.main:app --port 8001 &
sleep 2
curl -s -X POST http://localhost:8001/review/analyze \
  -H "Content-Type: application/json" \
  -d '{"frames": [{"id": "1", "name": "Test", "width": 100, "height": 100, "layers": []}]}' | python -m json.tool
pkill -f "uvicorn.*8001" 2>/dev/null || true
```
  </verify>
  <done>Server starts, POST /review/analyze returns stub AnalysisResult JSON, AsyncAzureOpenAI client accessible on request.app.state</done>
</task>

</tasks>

<verification>
After both tasks complete:

1. **Import check:**
```bash
cd /Users/chatdna/asw-frontend-accelerator/backend
python -c "from app.main import app; from app.models import DesignDataRequest, AnalysisResult; print('All imports OK')"
```

2. **Server startup:**
```bash
cd /Users/chatdna/asw-frontend-accelerator/backend
uvicorn app.main:app --port 8000
# Should see "Application startup complete" with no errors
```

3. **Endpoint test:**
```bash
curl -X POST http://localhost:8000/review/analyze \
  -H "Content-Type: application/json" \
  -d '{"frames": [{"id": "frame1", "name": "Login Screen", "width": 375, "height": 812, "layers": [{"id": "l1", "name": "Email Input", "type": "FRAME", "visible": true, "children": []}]}]}'
```
Expected: 200 OK with `{"findings": [], "summary": "Analysis pending - stub response", "frames_analyzed": 1}`

4. **Invalid request rejected:**
```bash
curl -X POST http://localhost:8000/review/analyze \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'
```
Expected: 422 Unprocessable Entity with validation error
</verification>

<success_criteria>
- POST /review/analyze endpoint accepts valid DesignDataRequest JSON
- Invalid requests return 422 with Pydantic validation errors
- Stub response returns AnalysisResult with empty findings
- AsyncAzureOpenAI client created at startup via lifespan
- API docs at /docs show the endpoint with request/response schemas
</success_criteria>

<output>
After completion, create `.planning/phases/2A-backend/2A-01-SUMMARY.md`
</output>
