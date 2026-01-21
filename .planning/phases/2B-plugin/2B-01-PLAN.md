---
phase: 2B-plugin
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - plugin/code.ts
  - plugin/code.js
autonomous: true

must_haves:
  truths:
    - "Plugin extracts layer hierarchy from selected frames"
    - "Plugin extracts fill colors as hex values"
    - "Plugin extracts text content, fontSize, fontFamily"
    - "Plugin handles figma.mixed values without crashing"
    - "Extraction respects depth limit to prevent stack overflow"
  artifacts:
    - path: "plugin/code.ts"
      provides: "Recursive layer extraction with type guards"
      contains: "extractLayer"
    - path: "plugin/code.js"
      provides: "Compiled extraction code"
  key_links:
    - from: "plugin/code.ts"
      to: "figma.currentPage.selection"
      via: "extractFrame function"
      pattern: "figma\\.currentPage\\.selection"
    - from: "plugin/code.ts"
      to: "figma.ui.postMessage"
      via: "design-data message type"
      pattern: "postMessage.*design-data"
---

<objective>
Expand Figma plugin sandbox code to extract comprehensive design data from selected frames.

Purpose: Enable the design analysis backend to receive complete layer hierarchy, colors, and typography data from Figma designs. This is the data extraction foundation that PLUG-02 requires.

Output: Updated plugin/code.ts with recursive extraction of layers, fills, strokes, and text properties.
</objective>

<execution_context>
@~/.claude/get-shit-done/workflows/execute-plan.md
@~/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/2B-plugin/2B-RESEARCH.md

# Existing plugin code to extend
@plugin/code.ts
@plugin/manifest.json
</context>

<tasks>

<task type="auto">
  <name>Task 1: Add TypeScript interfaces for extracted design data</name>
  <files>plugin/code.ts</files>
  <action>
Add interface definitions at the top of code.ts (after the showUI call):

```typescript
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
  color?: string;  // hex format #RRGGBB
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
```

These interfaces match the backend's expected payload structure and handle Figma's mixed values.
  </action>
  <verify>TypeScript compiles without errors: `cd plugin && npm run build`</verify>
  <done>Interfaces defined in code.ts, TypeScript compilation succeeds</done>
</task>

<task type="auto">
  <name>Task 2: Implement recursive layer extraction with type guards</name>
  <files>plugin/code.ts</files>
  <action>
Add helper function and extraction logic after the interfaces:

1. Add rgbToHex helper:
```typescript
function rgbToHex(color: RGB): string {
  const r = Math.round(color.r * 255);
  const g = Math.round(color.g * 255);
  const b = Math.round(color.b * 255);
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase();
}
```

2. Add extractLayer function with:
   - Depth parameter with max of 15 (prevent stack overflow)
   - Skip invisible layers (reduce payload size)
   - Extract fills: filter for SOLID type, convert RGB to hex, handle figma.mixed
   - Extract strokes: filter for SOLID type, get strokeWeight (handle mixed)
   - Extract text properties: characters, fontSize, fontFamily, fontStyle (handle figma.mixed for all)
   - Recursive children extraction with depth increment

3. Add extractFrame function:
   - Take SceneNode, call extractLayer on it
   - Return ExtractedFrame with id, name, width, height, layers array

Key pitfall avoidance:
- Always check `node.fills !== figma.mixed` before iterating
- Use `textNode.fontSize === figma.mixed ? 'mixed' : textNode.fontSize`
- Cast fontName to FontName type when not mixed: `(textNode.fontName as FontName).family`

See 2B-RESEARCH.md "Complete Frame Extraction (code.ts)" section for full implementation pattern.
  </action>
  <verify>TypeScript compiles: `cd plugin && npm run build`</verify>
  <done>extractLayer and extractFrame functions exist, handle all edge cases, compile successfully</done>
</task>

<task type="auto">
  <name>Task 3: Update message handler to use new extraction</name>
  <files>plugin/code.ts, plugin/code.js</files>
  <action>
Replace the existing `figma.ui.onmessage` handler:

1. On 'get-selection' message:
   - Check selection.length === 0, send error if empty
   - Filter selection to only FRAME, COMPONENT, or INSTANCE types (not individual shapes)
   - If no valid frames, send error: "Please select frames, components, or instances"
   - Map filtered nodes through extractFrame
   - Send via postMessage with type: 'design-data', data: { frames }

2. Add handler for 'analysis-complete' message:
   - Extract findingCount from msg.data
   - Call figma.notify() to show toast: "Analysis complete: X finding(s)"

3. Keep existing 'close' handler

4. Increase UI height from 300 to 500 in showUI call (more room for results)

After editing code.ts, compile: `cd plugin && npm run build`
  </action>
  <verify>
1. `cd plugin && npm run build` succeeds
2. code.js file updated with compiled extraction code
3. Grep for 'design-data' in code.js confirms new message type exists
  </verify>
  <done>
- Message handler sends full design data with type 'design-data'
- Filters selection to frames/components/instances only
- Shows toast notification on analysis complete
- UI window height increased to 500px
- code.js compiled and ready for Figma
  </done>
</task>

</tasks>

<verification>
1. TypeScript compilation succeeds without errors
2. code.js contains extractLayer and extractFrame functions
3. code.js sends 'design-data' message type (not 'selection-data')
4. Interfaces handle 'mixed' string literal for text properties
</verification>

<success_criteria>
- Plugin sandbox extracts complete layer hierarchy from selected frames
- Extraction includes: fills (hex colors), strokes, text properties
- figma.mixed values handled gracefully (converted to 'mixed' string)
- Depth limit prevents stack overflow on complex designs
- Compiled code.js ready for Figma to load
</success_criteria>

<output>
After completion, create `.planning/phases/2B-plugin/2B-01-SUMMARY.md`
</output>
