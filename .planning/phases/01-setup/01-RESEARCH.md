# Phase 1: Setup - Research

**Researched:** 2026-01-21
**Domain:** Project scaffolding (Python FastAPI backend, Figma plugin, Azure OpenAI)
**Confidence:** HIGH

## Summary

This phase establishes the development environment for a 6-person hackathon team building a Figma plugin with Python backend. The setup must be quick (30 minutes) and enable parallel work streams. Three primary workstreams need scaffolding: Python FastAPI backend with Azure OpenAI, Figma TypeScript plugin, and shared git repository structure.

The approach is straightforward: use standard tooling with minimal configuration. FastAPI provides async-first Python backend with built-in OpenAPI docs. Figma's built-in "Create new plugin" dialog generates working boilerplate. Azure OpenAI uses the standard `openai` Python library with the `AzureOpenAI` class.

**Primary recommendation:** Use Figma's built-in plugin creator (no external boilerplate), FastAPI with Pydantic Settings for backend, and a simple flat monorepo structure with `backend/` and `plugin/` folders.

## Standard Stack

The established libraries/tools for this domain:

### Backend Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| fastapi | 0.109+ | HTTP API framework | Async-first, auto OpenAPI docs, type validation |
| uvicorn | 0.27+ | ASGI server | Standard FastAPI server, hot reload |
| openai | 1.12+ | Azure OpenAI SDK | Official SDK, supports AzureOpenAI class |
| pydantic-settings | 2.1+ | Environment config | Type-safe settings, .env file support |
| python-dotenv | 1.0+ | .env file loading | Pairs with pydantic-settings |

### Plugin Core
| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| Figma Desktop App | Latest | Plugin development | Required for local plugin testing |
| TypeScript | 5.x | Plugin language | Figma's typed API, better error catching |
| Node.js | 22.x | Build tooling | Required for TypeScript compilation |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| httpx | 0.27+ | HTTP client | If backend needs to call external APIs |
| pytest | 8.0+ | Testing | Backend unit tests |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Figma built-in scaffold | create-figma-plugin | More features but slower setup, overkill for hackathon |
| Pydantic Settings | plain os.environ | Less type safety, manual validation |
| uvicorn | gunicorn+uvicorn | Gunicorn for production, uvicorn alone fine for hackathon |

**Installation (Backend):**
```bash
pip install fastapi uvicorn openai pydantic-settings python-dotenv
```

**Installation (Plugin):**
```bash
# No npm install needed for minimal setup
# TypeScript compiler via npm if using TS
npm install -g typescript
```

## Architecture Patterns

### Recommended Project Structure
```
asw-frontend-accelerator/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app, CORS, routes
│   │   ├── config.py         # Pydantic Settings
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── review.py     # Design review endpoints
│   ├── requirements.txt
│   ├── .env.example          # Template for env vars
│   └── .env                  # Actual secrets (gitignored)
├── plugin/
│   ├── manifest.json         # Figma plugin manifest
│   ├── code.ts               # Main plugin logic (sandbox)
│   ├── code.js               # Compiled output
│   ├── ui.html               # Plugin UI
│   └── tsconfig.json         # TypeScript config
├── docs/
│   └── README.md             # Setup instructions
├── .gitignore
└── README.md
```

### Pattern 1: FastAPI with Pydantic Settings
**What:** Type-safe configuration loading from environment variables
**When to use:** Always for FastAPI apps needing external config (API keys, URLs)
**Example:**
```python
# Source: https://fastapi.tiangolo.com/advanced/settings/
# backend/app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_deployment: str
    azure_openai_api_version: str = "2024-02-15-preview"

    model_config = SettingsConfigDict(env_file=".env")

# backend/app/main.py
from functools import lru_cache
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import Settings

app = FastAPI()

# CORS for Figma plugin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Figma plugins have null origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@lru_cache
def get_settings():
    return Settings()
```

### Pattern 2: Figma Plugin Minimal Structure
**What:** Two-file plugin architecture (sandbox + UI)
**When to use:** Always for Figma plugins
**Example:**
```json
// Source: https://developers.figma.com/docs/plugins/manifest/
// plugin/manifest.json
{
  "name": "Design Review AI",
  "id": "000000000000000000",
  "api": "1.0.0",
  "main": "code.js",
  "ui": "ui.html",
  "editorType": ["figma"],
  "networkAccess": {
    "allowedDomains": ["http://localhost:8000"],
    "reasoning": "Connect to local Python backend for AI review",
    "devAllowedDomains": ["http://localhost:*"]
  }
}
```

### Pattern 3: Azure OpenAI Connection
**What:** Using AzureOpenAI class from openai library
**When to use:** When connecting to Azure OpenAI (not direct OpenAI)
**Example:**
```python
# Source: https://github.com/openai/openai-python/blob/main/examples/azure.py
from openai import AzureOpenAI
import os

# Environment variables: AZURE_OPENAI_API_KEY (auto-loaded)
client = AzureOpenAI(
    api_version="2024-02-15-preview",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
)

# Test connection
completion = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=[{"role": "user", "content": "Say hello"}],
    max_tokens=10
)
print(completion.choices[0].message.content)
```

### Anti-Patterns to Avoid
- **Hardcoding API keys:** Always use environment variables
- **Missing CORS middleware:** Figma plugins will fail silently without it
- **Complex boilerplate:** For 30-min setup, use Figma's built-in scaffold, not external tools
- **Monolithic main.py:** Even for hackathon, separate config from routes

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Environment config | Manual os.environ parsing | pydantic-settings | Type validation, .env support, defaults |
| CORS handling | Custom headers | CORSMiddleware | Handles preflight, all edge cases |
| API client for Azure | Raw httpx/requests | openai library AzureOpenAI | Handles auth, retries, streaming |
| Plugin messaging | Custom postMessage wrapper | Figma's built-in pattern | Already in scaffold |
| TypeScript setup | Manual tsconfig | Figma's scaffold tsconfig | Pre-configured for plugin API |

**Key insight:** The hackathon time constraint means every minute counts. Built-in solutions and official scaffolds are pre-tested and documented.

## Common Pitfalls

### Pitfall 1: CORS Blocking Figma Plugin Requests
**What goes wrong:** Plugin makes fetch() to backend, gets CORS error, fails silently
**Why it happens:** Figma plugin iframes have `null` origin, most CORS configs don't allow this
**How to avoid:** Use `allow_origins=["*"]` in CORSMiddleware (acceptable for local dev)
**Warning signs:** Plugin UI loads but "submit" buttons do nothing

### Pitfall 2: Azure OpenAI 429 Rate Limits
**What goes wrong:** First few requests work, then API returns 429 errors
**Why it happens:** Azure OpenAI has tokens-per-minute limits, aggressive testing hits them
**How to avoid:** Add delay between test calls, cache responses during dev
**Warning signs:** "Rate limit exceeded" in API response

### Pitfall 3: Wrong Azure OpenAI Configuration
**What goes wrong:** "Resource not found" or "Invalid API key" errors
**Why it happens:** Using endpoint without deployment name, wrong API version, mixed up keys
**How to avoid:**
- Endpoint should be `https://{resource}.openai.azure.com/`
- Deployment name is NOT the model name (e.g., "my-gpt4" not "gpt-4")
- API version must be supported (use `2024-02-15-preview` or later)
**Warning signs:** 404 errors, authentication failures

### Pitfall 4: Figma Plugin ID Not Set
**What goes wrong:** Plugin loads once but can't be reloaded or shared
**Why it happens:** manifest.json has placeholder ID, not Figma-assigned ID
**How to avoid:** Create plugin via Figma UI first to get assigned ID
**Warning signs:** "Plugin already exists" errors on reload

### Pitfall 5: Missing networkAccess in Manifest
**What goes wrong:** fetch() calls fail with no error message
**Why it happens:** Figma blocks network calls not declared in manifest
**How to avoid:** Add all backend URLs to `allowedDomains` array, use `devAllowedDomains` for localhost
**Warning signs:** Network tab shows request blocked, no console error

### Pitfall 6: TypeScript Not Compiled
**What goes wrong:** Plugin shows old behavior, changes don't appear
**Why it happens:** Edited .ts file but manifest points to .js, forgot to compile
**How to avoid:** Run `tsc --watch` in terminal during development
**Warning signs:** Changes to code.ts have no effect

## Code Examples

Verified patterns from official sources:

### Backend: Complete main.py
```python
# backend/app/main.py
from functools import lru_cache
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AzureOpenAI
from .config import Settings

app = FastAPI(title="Design Review API")

# CORS - required for Figma plugin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@lru_cache
def get_settings():
    return Settings()

def get_openai_client(settings: Settings = Depends(get_settings)):
    return AzureOpenAI(
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
    )

@app.get("/health")
async def health():
    return {"status": "ok"}

class ReviewRequest(BaseModel):
    design_data: str

class ReviewResponse(BaseModel):
    feedback: str

@app.post("/review", response_model=ReviewResponse)
async def review_design(
    request: ReviewRequest,
    client: AzureOpenAI = Depends(get_openai_client),
    settings: Settings = Depends(get_settings),
):
    try:
        completion = client.chat.completions.create(
            model=settings.azure_openai_deployment,
            messages=[
                {"role": "system", "content": "You are a design reviewer."},
                {"role": "user", "content": request.design_data}
            ],
            max_tokens=500,
        )
        return ReviewResponse(feedback=completion.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Backend: config.py
```python
# backend/app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_openai_deployment: str
    azure_openai_api_version: str = "2024-02-15-preview"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
```

### Backend: .env.example
```bash
# backend/.env.example
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### Plugin: manifest.json
```json
{
  "name": "Design Review AI",
  "id": "000000000000000000",
  "api": "1.0.0",
  "main": "code.js",
  "ui": "ui.html",
  "editorType": ["figma"],
  "networkAccess": {
    "allowedDomains": ["http://localhost:8000"],
    "reasoning": "Connect to local Python backend",
    "devAllowedDomains": ["http://localhost:*", "http://127.0.0.1:*"]
  }
}
```

### Plugin: code.ts (sandbox)
```typescript
// plugin/code.ts
figma.showUI(__html__, { width: 400, height: 300 });

figma.ui.onmessage = async (msg: { type: string; data?: any }) => {
  if (msg.type === 'get-selection') {
    const selection = figma.currentPage.selection;
    if (selection.length === 0) {
      figma.ui.postMessage({ type: 'error', message: 'No selection' });
      return;
    }

    // Extract basic info from selection
    const data = selection.map(node => ({
      name: node.name,
      type: node.type,
      width: 'width' in node ? node.width : 0,
      height: 'height' in node ? node.height : 0,
    }));

    figma.ui.postMessage({ type: 'selection-data', data });
  }

  if (msg.type === 'close') {
    figma.closePlugin();
  }
};
```

### Plugin: ui.html
```html
<!-- plugin/ui.html -->
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Inter, sans-serif; padding: 16px; }
    button { padding: 8px 16px; margin: 4px; cursor: pointer; }
    #result { margin-top: 16px; white-space: pre-wrap; }
  </style>
</head>
<body>
  <h3>Design Review AI</h3>
  <button id="analyze">Analyze Selection</button>
  <div id="result"></div>

  <script>
    const resultDiv = document.getElementById('result');

    document.getElementById('analyze').onclick = () => {
      parent.postMessage({ pluginMessage: { type: 'get-selection' } }, '*');
    };

    window.onmessage = async (event) => {
      const msg = event.data.pluginMessage;

      if (msg.type === 'selection-data') {
        resultDiv.textContent = 'Sending to backend...';
        try {
          const response = await fetch('http://localhost:8000/review', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ design_data: JSON.stringify(msg.data) })
          });
          const result = await response.json();
          resultDiv.textContent = result.feedback;
        } catch (err) {
          resultDiv.textContent = 'Error: ' + err.message;
        }
      }

      if (msg.type === 'error') {
        resultDiv.textContent = 'Error: ' + msg.message;
      }
    };
  </script>
</body>
</html>
```

### Plugin: tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["ES2017"],
    "strict": true,
    "typeRoots": ["./node_modules/@types", "./node_modules/@figma"]
  },
  "files": ["code.ts"]
}
```

### Connection Test Script
```python
# backend/test_connection.py
"""Quick script to verify Azure OpenAI connection"""
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

try:
    completion = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[{"role": "user", "content": "Say 'connection successful'"}],
        max_tokens=10,
    )
    print("SUCCESS:", completion.choices[0].message.content)
except Exception as e:
    print("FAILED:", str(e))
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| os.environ manual | pydantic-settings | 2023 | Type safety, validation |
| sync requests | AzureOpenAI (httpx-based) | 2024 | Better async support |
| webpack for plugins | esbuild/Vite or vanilla | 2024 | Faster builds, simpler |

**Deprecated/outdated:**
- `openai<1.0` API: Pre-1.0 had different class structure, use 1.0+ patterns
- `azure-openai` separate package: Merged into main `openai` package

## Open Questions

Things that couldn't be fully resolved:

1. **Figma Plugin ID Assignment**
   - What we know: ID is assigned by Figma when you create plugin via UI
   - What's unclear: Exact flow in Figma desktop app for 2026
   - Recommendation: Have one team member create plugin via Figma UI, share manifest with real ID

2. **Azure OpenAI API Version**
   - What we know: `2024-02-15-preview` works, newer versions exist
   - What's unclear: Which version is latest stable for your Azure region
   - Recommendation: Start with `2024-02-15-preview`, update if needed

3. **Figma Plugin Type Definitions**
   - What we know: `@figma/plugin-typings` package exists
   - What's unclear: Whether included in Figma's scaffold or needs separate install
   - Recommendation: If scaffold doesn't include, run `npm install --save-dev @figma/plugin-typings`

## Sources

### Primary (HIGH confidence)
- [FastAPI Official Docs - Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/) - Project structure
- [FastAPI Official Docs - Settings](https://fastapi.tiangolo.com/advanced/settings/) - Pydantic Settings pattern
- [FastAPI Official Docs - CORS](https://fastapi.tiangolo.com/tutorial/cors/) - CORS middleware setup
- [Figma Plugin Manifest](https://developers.figma.com/docs/plugins/manifest/) - Manifest structure
- [OpenAI Python Examples - Azure](https://github.com/openai/openai-python/blob/main/examples/azure.py) - AzureOpenAI class

### Secondary (MEDIUM confidence)
- [Create Figma Plugin Quick Start](https://yuanqing.github.io/create-figma-plugin/quick-start/) - Alternative scaffold option
- [Azure OpenAI Quickstart](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart) - Environment setup
- [GitHub FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) - Community patterns

### Tertiary (LOW confidence)
- WebSearch results for monorepo structure - Community opinions, verify with team preferences

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Official documentation verified
- Architecture patterns: HIGH - FastAPI and Figma official docs
- Pitfalls: MEDIUM - Mix of official docs and community experience
- Code examples: HIGH - Adapted from official examples

**Research date:** 2026-01-21
**Valid until:** 2026-02-21 (30 days - stable technologies)
