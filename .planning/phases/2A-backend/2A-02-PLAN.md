---
phase: 2A-backend
plan: 02
type: execute
wave: 2
depends_on: ["2A-01"]
files_modified:
  - backend/app/services/__init__.py
  - backend/app/services/analyzer.py
  - backend/app/routers/review.py
  - backend/guidelines/GUIDELINES.md
autonomous: true

must_haves:
  truths:
    - "POST /review/analyze returns real Azure OpenAI analysis"
    - "Agent detects missing UI states (loading, error, empty, disabled, hover)"
    - "Agent detects accessibility gaps (contrast, labels, focus states)"
    - "Agent detects design system violations (spacing, colors, typography)"
    - "Agent detects responsiveness gaps when multiple frame widths present"
    - "Agent uses guidelines document for reference"
    - "Findings have severity (critical/warning/info) and recommendations"
  artifacts:
    - path: "backend/app/services/analyzer.py"
      provides: "analyze_design async function"
      exports: ["analyze_design"]
      min_lines: 50
    - path: "backend/guidelines/GUIDELINES.md"
      provides: "Placeholder design guidelines for agent reference"
      contains: "# Design Guidelines"
  key_links:
    - from: "backend/app/routers/review.py"
      to: "backend/app/services/analyzer.py"
      via: "import analyze_design"
      pattern: "from.*services.analyzer import"
    - from: "backend/app/services/analyzer.py"
      to: "openai.AsyncAzureOpenAI"
      via: "beta.chat.completions.parse"
      pattern: "beta\\.chat\\.completions\\.parse"
    - from: "backend/app/services/analyzer.py"
      to: "backend/guidelines/GUIDELINES.md"
      via: "Path read"
      pattern: "GUIDELINES.*read_text|open.*GUIDELINES"
---

<objective>
Implement the Azure OpenAI analysis agent that performs design review across four categories.

Purpose: Fulfill AGENT-01 through AGENT-05 requirements - the core intelligence that makes the tool valuable.
Output: Working analyzer that uses Azure OpenAI structured outputs to return categorized findings with severity and recommendations.
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
@.planning/phases/2A-backend/2A-01-SUMMARY.md

# Files from Plan 01
@backend/app/main.py
@backend/app/models/request.py
@backend/app/models/response.py
@backend/app/routers/review.py
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create placeholder guidelines and analyzer service</name>
  <files>
    backend/guidelines/GUIDELINES.md
    backend/app/services/__init__.py
    backend/app/services/analyzer.py
  </files>
  <action>
**Create backend/guidelines/GUIDELINES.md:**

Create a placeholder guidelines document that the agent will reference. This is a minimal version - Phase 2C will create the full document. Include sections for:
- UI States: List expected states (loading, error, empty, disabled, hover, focus, pressed)
- Accessibility: WCAG basics (contrast 4.5:1, labels, focus visible)
- Design System: Common spacing values (4, 8, 16, 24, 32px), color token expectations
- Responsiveness: Common breakpoints (320 mobile, 768 tablet, 1024 desktop, 1440 wide)

**Create backend/app/services/__init__.py:**
```python
from .analyzer import analyze_design

__all__ = ["analyze_design"]
```

**Create backend/app/services/analyzer.py:**

Follow the research pattern exactly:

1. Import Path from pathlib
2. Import AsyncAzureOpenAI from openai
3. Import models from `..models.request` and `..models.response`
4. Define GUIDELINES_PATH using `Path(__file__).parent.parent.parent / "guidelines" / "GUIDELINES.md"` (absolute path relative to file)
5. Define SYSTEM_PROMPT that:
   - Explains the agent is a design review expert
   - Lists four categories with specific items to check:
     - MISSING_STATES: loading, error, empty, disabled, hover, focus, pressed
     - ACCESSIBILITY: contrast ratios, labels, focus indicators, touch targets (44x44px min)
     - DESIGN_SYSTEM: spacing consistency (4px grid), color token usage, typography scale
     - RESPONSIVENESS: missing breakpoints when frames suggest responsive design
   - Explains severity levels:
     - critical: blocks users or causes accessibility failures
     - warning: degrades user experience
     - info: nice to fix, polish items
   - Instructs to provide actionable recommendations
   - Instructs to list affected frame names
6. Create `analyze_design` async function:
   - Parameters: client (AsyncAzureOpenAI), deployment (str), design_data (DesignDataRequest)
   - Load guidelines from file (handle FileNotFoundError gracefully - use empty string)
   - Allow override if design_data.guidelines is provided
   - Build user_prompt with guidelines + design data JSON
   - Call `client.beta.chat.completions.parse()` with:
     - model=deployment
     - messages=[system, user]
     - response_format=AnalysisResult
     - temperature=0.2 (for consistency)
   - Return `completion.choices[0].message.parsed`

Error handling: Let OpenAI exceptions propagate - router handles them.
  </action>
  <verify>
```bash
cd /Users/chatdna/asw-frontend-accelerator/backend
python -c "from app.services import analyze_design; print('Analyzer imports OK')"
ls -la guidelines/GUIDELINES.md
```
  </verify>
  <done>analyzer.py importable, GUIDELINES.md exists, SYSTEM_PROMPT covers all four categories</done>
</task>

<task type="auto">
  <name>Task 2: Wire analyzer to endpoint with error handling</name>
  <files>
    backend/app/routers/review.py
  </files>
  <action>
Update backend/app/routers/review.py to:

1. Import analyze_design from `..services.analyzer`
2. Import APIError and RateLimitError from openai
3. Replace stub response with actual analysis call:

```python
@router.post("/analyze", response_model=AnalysisResult)
async def analyze(request: Request, data: DesignDataRequest) -> AnalysisResult:
    """
    Analyze design data for completeness issues.

    Checks for:
    - Missing UI states (loading, error, empty, disabled, hover, focus, pressed)
    - Accessibility gaps (contrast, labels, focus indicators, touch targets)
    - Design system violations (spacing, colors, typography)
    - Responsiveness gaps (missing breakpoints)

    Returns structured findings with severity and recommendations.
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
    except RateLimitError:
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

The endpoint now makes real Azure OpenAI calls and returns structured analysis results.
  </action>
  <verify>
```bash
cd /Users/chatdna/asw-frontend-accelerator/backend

# Check syntax
python -c "from app.routers.review import router; print('Router imports OK')"

# Full integration test requires Azure OpenAI credentials
# If .env exists with valid credentials, test with:
if [ -f .env ]; then
  timeout 10 uvicorn app.main:app --port 8002 &
  sleep 3
  curl -s -X POST http://localhost:8002/review/analyze \
    -H "Content-Type: application/json" \
    -d '{"frames": [{"id": "1", "name": "Login Button", "width": 100, "height": 44, "layers": [{"id": "l1", "name": "Label", "type": "TEXT", "visible": true, "children": [], "text": {"content": "Login"}}]}]}' | head -c 500
  pkill -f "uvicorn.*8002" 2>/dev/null || true
else
  echo "No .env file - skipping live test (expected during CI)"
fi
```
  </verify>
  <done>Endpoint calls analyze_design, returns AnalysisResult with findings from Azure OpenAI, handles rate limits and API errors</done>
</task>

</tasks>

<verification>
After both tasks complete:

1. **Import chain:**
```bash
cd /Users/chatdna/asw-frontend-accelerator/backend
python -c "
from app.main import app
from app.services import analyze_design
from app.models import AnalysisResult, Finding, Severity, FindingCategory
print('All imports OK')
"
```

2. **Guidelines file exists:**
```bash
cat /Users/chatdna/asw-frontend-accelerator/backend/guidelines/GUIDELINES.md | head -20
```

3. **Server starts:**
```bash
cd /Users/chatdna/asw-frontend-accelerator/backend
# Requires valid .env with Azure OpenAI credentials
uvicorn app.main:app --port 8000
# Should see "Application startup complete"
```

4. **Full integration test (requires Azure OpenAI credentials):**
```bash
curl -X POST http://localhost:8000/review/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "frames": [
      {
        "id": "frame1",
        "name": "Login Form",
        "width": 375,
        "height": 600,
        "layers": [
          {"id": "l1", "name": "Email Input", "type": "FRAME", "visible": true, "children": []},
          {"id": "l2", "name": "Password Input", "type": "FRAME", "visible": true, "children": []},
          {"id": "l3", "name": "Submit Button", "type": "FRAME", "visible": true, "children": []}
        ]
      }
    ]
  }'
```
Expected: 200 OK with findings array containing categorized issues (missing states, a11y, etc.)

5. **OpenAPI docs:**
Visit http://localhost:8000/docs - should show /review/analyze with full request/response schemas.
</verification>

<success_criteria>
- analyze_design function makes Azure OpenAI call with structured output
- Agent uses GUIDELINES.md for reference (AGENT-05)
- Response contains findings with category (MISSING_STATES/ACCESSIBILITY/DESIGN_SYSTEM/RESPONSIVENESS)
- Each finding has severity (critical/warning/info) and recommendation
- Rate limit errors return 429 with helpful message
- API errors return 502 with error details
- All 9 Phase 2A requirements satisfied: API-01, API-02, API-03, API-04, AGENT-01, AGENT-02, AGENT-03, AGENT-04, AGENT-05
</success_criteria>

<output>
After completion, create `.planning/phases/2A-backend/2A-02-SUMMARY.md`
</output>
