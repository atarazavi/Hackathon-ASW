# Phase 2B: Plugin - Research

**Researched:** 2026-01-21
**Domain:** Figma Plugin API - Design Data Extraction and HTTP Communication
**Confidence:** HIGH

## Summary

Phase 2B extends the existing Figma plugin from Phase 1 to extract comprehensive design data from selected frames and call the backend API. The existing plugin has basic selection handling (name, type, width, height) and needs to be expanded to extract layers, styles (colors, typography), and design tokens.

The Figma Plugin architecture has two environments that communicate via `postMessage`:
1. **Sandbox (code.ts)** - Accesses Figma document, extracts design data
2. **UI (ui.html)** - Makes HTTP requests to backend, displays results

Key technical challenges:
1. Recursive traversal of frame children to extract all layers
2. Extracting fill colors, text styles, and effects from nodes
3. Handling `figma.mixed` values for properties with mixed styles
4. Making POST requests to the backend API from the UI iframe

**Primary recommendation:** Extract design data in code.ts using recursive traversal with type guards. Send data to UI via `postMessage`. Make HTTP fetch calls from ui.html since it has browser API access. Use `figma.util.rgb()` utilities for color conversion.

## Standard Stack

### Core (Already Exists)
| Technology | Purpose | Status |
|------------|---------|--------|
| TypeScript | Plugin sandbox code | Exists in `plugin/code.ts` |
| HTML/JS | UI iframe | Exists in `plugin/ui.html` |
| Figma Plugin API | Design data access | v1.0.0 (in manifest) |

### No Additional Libraries Needed

The Figma Plugin API provides everything needed:
- `figma.currentPage.selection` - Get selected nodes
- `figma.util.rgb()` / `figma.util.rgba()` - Color conversion utilities
- Node traversal via `children` property
- Built-in `fetch` API for HTTP requests in UI

### Why No External Dependencies

| Library | Why NOT |
|---------|---------|
| `figma-plugin-helpers` | Adds complexity, built-in utils are sufficient |
| `figwire` / `figma-connect` | Overkill for simple message passing |
| `axios` | Native `fetch` works fine in UI iframe |

**The existing plugin structure is correct. Extend it, don't replace it.**

## Architecture Patterns

### Recommended Code Structure

```
plugin/
├── manifest.json          # (exists) - networkAccess already configured
├── code.ts                # (exists) - Sandbox: extend to extract full design data
├── code.js                # (compiled) - Don't edit directly
├── ui.html                # (exists) - UI: add fetch call to backend
└── tsconfig.json          # (if needed for TypeScript compilation)
```

### Pattern 1: Recursive Node Traversal

**What:** Extract all layers from selected frames using recursive traversal.
**When to use:** When extracting complete design data from frame hierarchies.

```typescript
// code.ts - in sandbox
interface ExtractedLayer {
  id: string;
  name: string;
  type: string;
  visible: boolean;
  x: number;
  y: number;
  width: number;
  height: number;
  opacity: number;
  fills: ExtractedFill[];
  children: ExtractedLayer[];
  // Text-specific
  text?: {
    content: string;
    fontSize: number | 'mixed';
    fontFamily: string | 'mixed';
    fontWeight: string | 'mixed';
  };
}

interface ExtractedFill {
  type: 'SOLID' | 'GRADIENT' | 'IMAGE' | string;
  color?: string;  // hex color for SOLID fills
  opacity: number;
}

function extractLayer(node: SceneNode): ExtractedLayer {
  const layer: ExtractedLayer = {
    id: node.id,
    name: node.name,
    type: node.type,
    visible: 'visible' in node ? node.visible : true,
    x: 'x' in node ? node.x : 0,
    y: 'y' in node ? node.y : 0,
    width: 'width' in node ? node.width : 0,
    height: 'height' in node ? node.height : 0,
    opacity: 'opacity' in node ? node.opacity : 1,
    fills: [],
    children: [],
  };

  // Extract fills (colors)
  if ('fills' in node && node.fills !== figma.mixed) {
    layer.fills = (node.fills as readonly Paint[])
      .filter((fill): fill is SolidPaint => fill.type === 'SOLID')
      .map(fill => ({
        type: 'SOLID',
        color: rgbToHex(fill.color),
        opacity: fill.opacity ?? 1,
      }));
  }

  // Extract text properties
  if (node.type === 'TEXT') {
    const textNode = node as TextNode;
    layer.text = {
      content: textNode.characters,
      fontSize: textNode.fontSize === figma.mixed ? 'mixed' : textNode.fontSize,
      fontFamily: textNode.fontName === figma.mixed ? 'mixed' : (textNode.fontName as FontName).family,
      fontWeight: textNode.fontName === figma.mixed ? 'mixed' : (textNode.fontName as FontName).style,
    };
  }

  // Recursively extract children
  if ('children' in node) {
    layer.children = (node.children as SceneNode[]).map(extractLayer);
  }

  return layer;
}

// Helper: Convert Figma RGB (0-1) to hex
function rgbToHex(color: RGB): string {
  const r = Math.round(color.r * 255);
  const g = Math.round(color.g * 255);
  const b = Math.round(color.b * 255);
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
}
```

### Pattern 2: Two-Way Message Passing

**What:** Communication between sandbox (code.ts) and UI (ui.html).
**When to use:** Always - this is how Figma plugins work.

```typescript
// code.ts - Send extracted data to UI
figma.ui.postMessage({
  type: 'design-data',
  data: {
    frames: extractedFrames,
    timestamp: Date.now(),
  }
});

// code.ts - Receive messages from UI
figma.ui.onmessage = async (msg: { type: string; data?: any }) => {
  if (msg.type === 'get-selection') {
    // Extract and send design data
    const frames = figma.currentPage.selection
      .filter(node => node.type === 'FRAME' || node.type === 'COMPONENT' || node.type === 'INSTANCE')
      .map(extractFrame);

    figma.ui.postMessage({ type: 'design-data', data: { frames } });
  }

  if (msg.type === 'analysis-complete') {
    figma.notify(`Analysis complete: ${msg.data.findingCount} findings`);
  }
};
```

```html
<!-- ui.html - Send messages to sandbox -->
<script>
  // Request data from sandbox
  parent.postMessage({ pluginMessage: { type: 'get-selection' } }, '*');

  // Receive messages from sandbox
  window.onmessage = async (event) => {
    const msg = event.data.pluginMessage;
    if (msg?.type === 'design-data') {
      await analyzeDesign(msg.data);
    }
  };
</script>
```

### Pattern 3: HTTP Request from UI

**What:** Make POST request to backend from UI iframe.
**When to use:** For calling the backend API - only works from ui.html.

```html
<!-- ui.html -->
<script>
async function analyzeDesign(designData) {
  const resultDiv = document.getElementById('result');
  resultDiv.textContent = 'Analyzing design...';

  try {
    const response = await fetch('http://localhost:8000/review/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(designData),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const result = await response.json();
    displayFindings(result);

    // Notify sandbox of completion
    parent.postMessage({
      pluginMessage: {
        type: 'analysis-complete',
        data: { findingCount: result.findings.length }
      }
    }, '*');
  } catch (error) {
    resultDiv.innerHTML = `<span class="error">Error: ${error.message}</span>`;
  }
}
</script>
```

### Anti-Patterns to Avoid

- **Making fetch from code.ts:** The sandbox cannot use browser fetch. Network requests MUST go through ui.html.
- **Using `'fills' in node` for type checks:** Use `node.type === 'FRAME'` instead - more reliable with TypeScript.
- **Ignoring `figma.mixed`:** Always check if a property returns `figma.mixed` before using it.
- **Deep recursion without limits:** Add a depth limit to prevent stack overflow on deeply nested frames.
- **Blocking the main thread:** Use async/await properly; Figma will kill long-running sync operations.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| RGB to Hex conversion | Complex string formatting | Simple `rgbToHex()` helper (shown above) | Figma returns 0-1 floats, easy to convert |
| Color parsing | Regex-based parsing | `figma.util.rgb()` / `figma.util.rgba()` | Built-in, handles CSS strings |
| Node type checking | String-based checks | TypeScript type guards + `node.type` | Type-safe, better autocomplete |
| Message serialization | Custom JSON handling | postMessage handles it | Automatic serialization of most types |

**Key insight:** Figma's Plugin API already provides utilities for common operations. Check `figma.util.*` before writing helpers.

## Common Pitfalls

### Pitfall 1: Accessing Properties That Don't Exist on Node Type

**What goes wrong:** TypeError when accessing `.fills` on a GroupNode or `.children` on a TextNode.
**Why it happens:** Different node types have different properties. GroupNode doesn't have fills.
**How to avoid:** Always check node.type before accessing type-specific properties.
**Warning signs:** "Cannot read property 'fills' of undefined" or similar TypeScript errors.

```typescript
// WRONG
const fills = node.fills;  // Crashes if node is GroupNode

// RIGHT
if (node.type === 'FRAME' || node.type === 'RECTANGLE') {
  const fills = node.fills;  // TypeScript knows fills exists
}
```

### Pitfall 2: Forgetting to Handle `figma.mixed`

**What goes wrong:** Code assumes number but gets `figma.mixed` symbol.
**Why it happens:** Text nodes with mixed styles return `figma.mixed` for fontSize, fontName, etc.
**How to avoid:** Always check `=== figma.mixed` before using the value.
**Warning signs:** "Cannot read properties of Symbol(mixed)" or JSON serialization errors.

```typescript
// WRONG
const fontSize = textNode.fontSize;  // Could be figma.mixed

// RIGHT
const fontSize = textNode.fontSize === figma.mixed
  ? 'mixed'
  : textNode.fontSize;
```

### Pitfall 3: CORS Errors When Calling Backend

**What goes wrong:** "Access to fetch blocked by CORS policy" error.
**Why it happens:** Plugin iframe has `null` origin; backend must allow `Access-Control-Allow-Origin: *`.
**How to avoid:** Backend already has this configured (checked in Phase 2A research). Verify CORS middleware.
**Warning signs:** Network request shows "CORS error" in browser console.

```python
# Backend (already configured in main.py)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Required for Figma plugin null origin
    ...
)
```

### Pitfall 4: networkAccess Domain Mismatch

**What goes wrong:** Content Security Policy (CSP) error blocks network request.
**Why it happens:** The domain in manifest.json `allowedDomains` must match the actual URL.
**How to avoid:** Verify manifest includes `http://localhost:8000` (already configured).
**Warning signs:** "Refused to connect to 'http://...' because it violates the Content Security Policy".

```json
// manifest.json (already correct)
"networkAccess": {
  "allowedDomains": ["http://localhost:8000"]
}
```

### Pitfall 5: Large Payload Timeout

**What goes wrong:** Request times out or Figma becomes unresponsive with large designs.
**Why it happens:** Extracting every layer from complex designs produces huge JSON payloads.
**How to avoid:** Limit recursion depth, skip invisible layers, summarize rather than serialize everything.
**Warning signs:** Plugin hangs when selecting complex frames, browser memory spike.

```typescript
// Add depth limit to extraction
function extractLayer(node: SceneNode, depth: number = 0, maxDepth: number = 10): ExtractedLayer | null {
  if (depth > maxDepth) return null;  // Stop deep recursion
  if ('visible' in node && !node.visible) return null;  // Skip hidden layers
  // ... rest of extraction
}
```

### Pitfall 6: Serialization of Non-JSON Types

**What goes wrong:** postMessage fails or data is corrupted.
**Why it happens:** Trying to send functions, circular references, or special Figma objects.
**How to avoid:** Only send plain objects with primitive values, arrays, and nested objects.
**Warning signs:** "Failed to execute 'postMessage'" or silently missing data.

```typescript
// WRONG - node reference can't be serialized
figma.ui.postMessage({ node: selectedNode });

// RIGHT - extract only serializable data
figma.ui.postMessage({
  id: selectedNode.id,
  name: selectedNode.name,
  type: selectedNode.type,
});
```

## Code Examples

### Complete Frame Extraction (code.ts)

```typescript
// Design Review AI - Main plugin code (sandbox)
figma.showUI(__html__, { width: 400, height: 500 });

// Type definitions
interface ExtractedFrame {
  id: string;
  name: string;
  width: number;
  height: number;
  layers: ExtractedLayer[];
}

interface ExtractedLayer {
  id: string;
  name: string;
  type: string;
  visible: boolean;
  x: number;
  y: number;
  width: number;
  height: number;
  opacity: number;
  fills: ExtractedFill[];
  strokes: ExtractedStroke[];
  children: ExtractedLayer[];
  text?: ExtractedText;
}

interface ExtractedFill {
  type: string;
  color?: string;
  opacity: number;
}

interface ExtractedStroke {
  type: string;
  color?: string;
  weight: number;
}

interface ExtractedText {
  content: string;
  fontSize: number | 'mixed';
  fontFamily: string | 'mixed';
  fontStyle: string | 'mixed';
  fillColor?: string;
}

// Helper: RGB to Hex
function rgbToHex(color: RGB): string {
  const r = Math.round(color.r * 255);
  const g = Math.round(color.g * 255);
  const b = Math.round(color.b * 255);
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase();
}

// Extract a single layer with all its properties
function extractLayer(node: SceneNode, depth: number = 0): ExtractedLayer | null {
  // Limit recursion depth to prevent stack overflow
  if (depth > 15) return null;

  // Skip invisible layers to reduce payload
  if ('visible' in node && !node.visible) return null;

  const layer: ExtractedLayer = {
    id: node.id,
    name: node.name,
    type: node.type,
    visible: 'visible' in node ? node.visible : true,
    x: 'x' in node ? node.x : 0,
    y: 'y' in node ? node.y : 0,
    width: 'width' in node ? node.width : 0,
    height: 'height' in node ? node.height : 0,
    opacity: 'opacity' in node ? node.opacity : 1,
    fills: [],
    strokes: [],
    children: [],
  };

  // Extract fills (solid colors only for simplicity)
  if ('fills' in node && node.fills !== figma.mixed && Array.isArray(node.fills)) {
    layer.fills = (node.fills as readonly Paint[])
      .filter((fill): fill is SolidPaint => fill.type === 'SOLID' && fill.visible !== false)
      .map(fill => ({
        type: 'SOLID',
        color: rgbToHex(fill.color),
        opacity: fill.opacity ?? 1,
      }));
  }

  // Extract strokes
  if ('strokes' in node && Array.isArray(node.strokes)) {
    const strokeWeight = 'strokeWeight' in node ?
      (node.strokeWeight === figma.mixed ? 1 : node.strokeWeight as number) : 0;
    layer.strokes = (node.strokes as readonly Paint[])
      .filter((stroke): stroke is SolidPaint => stroke.type === 'SOLID' && stroke.visible !== false)
      .map(stroke => ({
        type: 'SOLID',
        color: rgbToHex(stroke.color),
        weight: strokeWeight,
      }));
  }

  // Extract text properties
  if (node.type === 'TEXT') {
    const textNode = node as TextNode;
    layer.text = {
      content: textNode.characters,
      fontSize: textNode.fontSize === figma.mixed ? 'mixed' : textNode.fontSize,
      fontFamily: textNode.fontName === figma.mixed ? 'mixed' : (textNode.fontName as FontName).family,
      fontStyle: textNode.fontName === figma.mixed ? 'mixed' : (textNode.fontName as FontName).style,
    };

    // Get text fill color (first solid fill)
    if (textNode.fills !== figma.mixed && Array.isArray(textNode.fills)) {
      const solidFill = (textNode.fills as Paint[]).find(
        (f): f is SolidPaint => f.type === 'SOLID'
      );
      if (solidFill) {
        layer.text.fillColor = rgbToHex(solidFill.color);
      }
    }
  }

  // Recursively extract children
  if ('children' in node) {
    layer.children = (node.children as SceneNode[])
      .map(child => extractLayer(child, depth + 1))
      .filter((child): child is ExtractedLayer => child !== null);
  }

  return layer;
}

// Extract a complete frame
function extractFrame(node: SceneNode): ExtractedFrame {
  const layers = extractLayer(node);
  return {
    id: node.id,
    name: node.name,
    width: 'width' in node ? node.width : 0,
    height: 'height' in node ? node.height : 0,
    layers: layers ? [layers] : [],
  };
}

// Message handler
figma.ui.onmessage = async (msg: { type: string; data?: any }) => {
  if (msg.type === 'get-selection') {
    const selection = figma.currentPage.selection;

    if (selection.length === 0) {
      figma.ui.postMessage({
        type: 'error',
        message: 'No frames selected. Please select one or more frames.'
      });
      return;
    }

    // Filter to only frames/components/instances (not individual shapes)
    const frameNodes = selection.filter(
      node => node.type === 'FRAME' || node.type === 'COMPONENT' || node.type === 'INSTANCE'
    );

    if (frameNodes.length === 0) {
      figma.ui.postMessage({
        type: 'error',
        message: 'Please select frames, components, or instances (not individual shapes).'
      });
      return;
    }

    // Extract design data from all selected frames
    const frames = frameNodes.map(extractFrame);

    figma.ui.postMessage({
      type: 'design-data',
      data: { frames }
    });
  }

  if (msg.type === 'analysis-complete') {
    const findingCount = msg.data?.findingCount ?? 0;
    figma.notify(`Analysis complete: ${findingCount} finding(s)`);
  }

  if (msg.type === 'close') {
    figma.closePlugin();
  }
};
```

### Complete UI with API Call (ui.html)

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: Inter, system-ui, sans-serif;
      padding: 16px;
      margin: 0;
    }
    h3 {
      margin: 0 0 16px 0;
      font-size: 14px;
      font-weight: 600;
    }
    button {
      padding: 10px 16px;
      margin: 4px 0;
      cursor: pointer;
      background: #18A0FB;
      color: white;
      border: none;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 500;
      width: 100%;
    }
    button:hover {
      background: #0D8DE8;
    }
    button:disabled {
      background: #B3B3B3;
      cursor: not-allowed;
    }
    #result {
      margin-top: 16px;
      padding: 12px;
      background: #F5F5F5;
      border-radius: 6px;
      font-size: 12px;
      white-space: pre-wrap;
      min-height: 100px;
      max-height: 350px;
      overflow-y: auto;
    }
    .error {
      color: #F24822;
    }
    .loading {
      color: #666;
      font-style: italic;
    }
  </style>
</head>
<body>
  <h3>Design Review AI</h3>
  <button id="analyze">Review Selection</button>
  <div id="result">Select frames and click "Review Selection" to analyze.</div>

  <script>
    const resultDiv = document.getElementById('result');
    const analyzeBtn = document.getElementById('analyze');

    const BACKEND_URL = 'http://localhost:8000';

    // Request design data from sandbox
    analyzeBtn.addEventListener('click', () => {
      analyzeBtn.disabled = true;
      resultDiv.textContent = 'Extracting design data...';
      resultDiv.className = 'loading';
      parent.postMessage({ pluginMessage: { type: 'get-selection' } }, '*');
    });

    // Call backend API
    async function analyzeDesign(designData) {
      resultDiv.textContent = 'Analyzing design with AI...';

      try {
        const response = await fetch(`${BACKEND_URL}/review/analyze`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(designData),
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Server error (${response.status}): ${errorText}`);
        }

        const result = await response.json();
        displayResult(result);

        // Notify sandbox
        parent.postMessage({
          pluginMessage: {
            type: 'analysis-complete',
            data: { findingCount: result.findings?.length ?? 0 }
          }
        }, '*');

      } catch (error) {
        resultDiv.className = 'error';
        if (error.message.includes('Failed to fetch')) {
          resultDiv.textContent = `Error: Cannot connect to backend.\n\nMake sure the backend is running:\ncd backend && uvicorn app.main:app --reload`;
        } else {
          resultDiv.textContent = `Error: ${error.message}`;
        }
      } finally {
        analyzeBtn.disabled = false;
      }
    }

    // Display analysis results
    function displayResult(result) {
      resultDiv.className = '';

      if (!result.findings || result.findings.length === 0) {
        resultDiv.textContent = `No issues found!\n\nFrames analyzed: ${result.frames_analyzed}\n\n${result.summary || 'Design looks good.'}`;
        return;
      }

      let output = `Found ${result.findings.length} issue(s)\n`;
      output += `Frames analyzed: ${result.frames_analyzed}\n\n`;

      result.findings.forEach((finding, i) => {
        output += `${i + 1}. [${finding.severity.toUpperCase()}] ${finding.title}\n`;
        output += `   Category: ${finding.category}\n`;
        output += `   ${finding.description}\n`;
        output += `   Fix: ${finding.recommendation}\n\n`;
      });

      if (result.summary) {
        output += `Summary: ${result.summary}`;
      }

      resultDiv.textContent = output;
    }

    // Handle messages from sandbox
    window.onmessage = async (event) => {
      const msg = event.data.pluginMessage;
      if (!msg) return;

      if (msg.type === 'design-data') {
        await analyzeDesign(msg.data);
      }

      if (msg.type === 'error') {
        resultDiv.className = 'error';
        resultDiv.textContent = `Error: ${msg.message}`;
        analyzeBtn.disabled = false;
      }
    };
  </script>
</body>
</html>
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual RGB math | `figma.util.rgb()` / `figma.util.rgba()` | 2023 (Update 72) | Cleaner color handling |
| String-based type checks | `node.type === 'FRAME'` | Always preferred | Type-safe, better TS support |
| Sync operations | Async/await pattern | Figma API v1 | Required for non-blocking |
| XML manifest | JSON manifest | Figma API v1 | Standard format |

**Current best practices (2026):**
- Use TypeScript for better type safety with Figma's typed API
- Always handle `figma.mixed` for text properties
- Limit recursion depth for complex designs
- Keep sandbox code minimal, do heavy lifting in UI

## Open Questions

### 1. Optimal Extraction Depth

**What we know:** Deep recursion can cause performance issues.
**What's unclear:** What's the optimal max depth for design analysis?
**Recommendation:** Start with depth 15 (covers most real designs). Adjust based on demo performance.

### 2. Which Properties Matter Most for Analysis

**What we know:** Backend analyzes for missing states, accessibility, design system, responsiveness.
**What's unclear:** Which specific properties are most valuable for each analysis type?
**Recommendation:** Extract comprehensive data first, let the AI agent decide relevance. Include:
- All fills (for color analysis)
- Text properties (for accessibility/typography)
- Frame dimensions (for responsiveness)
- Layer names (for state detection via naming conventions)

### 3. Component Instance Handling

**What we know:** ComponentInstance nodes reference main components.
**What's unclear:** Should we extract main component data or just instance overrides?
**Recommendation:** Treat instances as regular frames for MVP. The AI doesn't need component relationships.

## Sources

### Primary (HIGH confidence)
- [Figma Plugin API - Accessing Document](https://developers.figma.com/docs/plugins/accessing-document/) - Node traversal, selection
- [Figma Plugin API - Working with Text](https://developers.figma.com/docs/plugins/working-with-text/) - TextNode, mixed styles
- [Figma Plugin API - Making Network Requests](https://developers.figma.com/docs/plugins/making-network-requests/) - fetch, manifest config
- [Figma Plugin API - How Plugins Run](https://developers.figma.com/docs/plugins/how-plugins-run/) - Sandbox/UI architecture
- [Figma Plugin API - FrameNode](https://developers.figma.com/docs/plugins/api/FrameNode/) - Frame properties
- [Figma Plugin API - fills property](https://developers.figma.com/docs/plugins/api/properties/nodes-fills/) - Paint types
- [Figma Plugin API - figma.util](https://developers.figma.com/docs/plugins/api/figma-util/) - Color utilities
- [Figma Plugin API - postMessage](https://developers.figma.com/docs/plugins/api/properties/figma-ui-postmessage/) - Message passing

### Secondary (MEDIUM confidence)
- [Figma Forum - Get styles from nodes](https://forum.figma.com/t/how-do-i-get-the-styles-of-nodes/606) - Style extraction patterns
- [Figma Forum - Color variables](https://forum.figma.com/ask-the-community-7/how-to-get-the-applied-color-variable-in-a-figma-plugin-37783) - Variable bindings

### Tertiary (LOW confidence)
- [Evil Martians - Advanced Figma Plugins](https://evilmartians.com/chronicles/figma-plugin-api-dive-into-advanced-algorithms-and-data-structures) - Traversal patterns
- [figwire package](https://www.npmjs.com/package/figwire) - For future type-safe messaging (not needed for MVP)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Using existing Figma Plugin API, no new dependencies
- Architecture: HIGH - Sandbox/UI pattern is well-documented
- Data extraction: HIGH - Properties and traversal verified with official docs
- API integration: HIGH - fetch works from UI, CORS already configured in backend
- Pitfalls: HIGH - Common issues documented in Figma forums

**Research date:** 2026-01-21
**Valid until:** 2026-02-21 (30 days - Figma Plugin API is stable)
