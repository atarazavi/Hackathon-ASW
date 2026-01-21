---
phase: 2B-plugin
plan: 02
type: execute
wave: 2
depends_on: ["2B-01"]
files_modified:
  - plugin/ui.html
autonomous: false

must_haves:
  truths:
    - "Plugin UI calls backend /analyze endpoint with design data"
    - "Plugin shows loading state while analyzing"
    - "Plugin displays analysis results (findings count, summary)"
    - "Connection errors show helpful message about backend"
    - "Button is disabled during analysis to prevent double-submit"
  artifacts:
    - path: "plugin/ui.html"
      provides: "API client with fetch to backend"
      contains: "fetch.*localhost:8000"
  key_links:
    - from: "plugin/ui.html"
      to: "http://localhost:8000/review/analyze"
      via: "fetch POST request"
      pattern: "fetch.*review/analyze"
    - from: "plugin/ui.html"
      to: "parent.postMessage"
      via: "analysis-complete notification"
      pattern: "analysis-complete"
---

<objective>
Wire plugin UI to call backend API with extracted design data and display results.

Purpose: Complete the plugin-to-backend communication flow required by PLUG-03. Designers can now click "Review Selection" and see analysis results from the AI backend.

Output: Updated plugin/ui.html with fetch call to /review/analyze endpoint and result display.
</objective>

<execution_context>
@~/.claude/get-shit-done/workflows/execute-plan.md
@~/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/2B-plugin/2B-RESEARCH.md

# Plugin UI to extend
@plugin/ui.html

# Prior plan output (extraction logic)
@.planning/phases/2B-plugin/2B-01-SUMMARY.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Add API client and result display to ui.html</name>
  <files>plugin/ui.html</files>
  <action>
Update ui.html to add backend communication:

1. Add CSS for loading and disabled states:
```css
.loading {
  color: #666;
  font-style: italic;
}
button:disabled {
  background: #B3B3B3;
  cursor: not-allowed;
}
```

2. Add BACKEND_URL constant at top of script:
```javascript
const BACKEND_URL = 'http://localhost:8000';
```

3. Update button click handler:
   - Disable button immediately
   - Show "Extracting design data..." loading state
   - Keep the postMessage call to sandbox

4. Add analyzeDesign async function:
   - Show "Analyzing design with AI..." loading state
   - POST to `${BACKEND_URL}/review/analyze` with JSON body
   - Handle response.ok check, parse JSON
   - Call displayResult() on success
   - Notify sandbox with 'analysis-complete' message and findingCount
   - On error: check for "Failed to fetch" and show helpful backend message
   - Re-enable button in finally block

5. Add displayResult function:
   - Show findings count and frames analyzed
   - Loop through findings, show: severity, title, category, description, recommendation
   - Show summary if present
   - Handle empty findings case: "No issues found!"

6. Update window.onmessage handler:
   - Change 'selection-data' to 'design-data' (matches 2B-01 change)
   - Call analyzeDesign(msg.data) instead of just displaying JSON
   - Re-enable button on error messages

See 2B-RESEARCH.md "Complete UI with API Call (ui.html)" section for full implementation pattern.
  </action>
  <verify>
1. ui.html is valid HTML (no syntax errors)
2. Contains fetch call to localhost:8000/review/analyze
3. Contains displayResult function
4. Contains analyzeDesign function
  </verify>
  <done>
- ui.html calls backend /review/analyze endpoint
- Loading states show during extraction and analysis
- Results display with severity, category, description, recommendation
- Connection errors show helpful message about starting backend
- Button disabled during analysis
  </done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>
Complete plugin data extraction and backend communication:
- code.ts extracts full layer hierarchy, fills, strokes, text from selected frames
- ui.html sends extracted data to backend and displays results
  </what-built>
  <how-to-verify>
**Prerequisite:** Backend must be running for full test.

1. Start backend (if not running):
   ```bash
   cd backend && source venv/bin/activate && uvicorn app.main:app --reload
   ```

2. Open Figma Desktop app

3. In any file, create or select a frame with:
   - Some rectangles with fill colors
   - Some text elements
   - Nested groups or frames (optional)

4. Open Plugin: Plugins > Development > Design Review AI

5. Click "Review Selection" button

6. Observe:
   - Button should disable
   - "Extracting design data..." should appear
   - "Analyzing design with AI..." should appear
   - After a moment, results should display:
     - Finding count
     - Frames analyzed count
     - Individual findings with severity/category/recommendation
   - Figma toast notification should appear

7. Test error handling:
   - Stop the backend
   - Click "Review Selection" again
   - Should show helpful error about backend not running

**Expected outcome:** Plugin successfully sends design data to backend and displays structured findings.
  </how-to-verify>
  <resume-signal>Type "approved" if plugin works end-to-end, or describe issues found</resume-signal>
</task>

</tasks>

<verification>
1. ui.html contains fetch POST to /review/analyze
2. Loading states appear during analysis
3. Results display findings from backend
4. Error handling shows helpful messages
5. End-to-end flow works: select frame > click Review > see findings
</verification>

<success_criteria>
- PLUG-01: Designer can select frames and trigger review (button click)
- PLUG-02: Plugin extracts layers, styles, tokens (via 2B-01)
- PLUG-03: Plugin calls backend API with extracted data (this plan)
- Full round-trip: selection > extraction > API call > results display
</success_criteria>

<output>
After completion, create `.planning/phases/2B-plugin/2B-02-SUMMARY.md`
</output>
