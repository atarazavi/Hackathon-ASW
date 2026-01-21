---
phase: 2C-assets
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - backend/guidelines/GUIDELINES.md
autonomous: true

must_haves:
  truths:
    - "GUIDELINES.md exists at backend/guidelines/GUIDELINES.md"
    - "Guidelines document covers all four analysis categories (states, a11y, design system, responsiveness)"
    - "Guidelines contain specific measurable values (4.5:1 contrast, 44px targets, spacing scale)"
    - "Guidelines structure is optimized for LLM parsing (tables, checklists)"
    - "Custom rules section exists for company-specific additions"
  artifacts:
    - path: "backend/guidelines/GUIDELINES.md"
      provides: "Design standards for AI analyzer reference"
      min_lines: 150
      contains: "## UI States"
  key_links:
    - from: "backend/guidelines/GUIDELINES.md"
      to: "backend/app/services/analyzer.py"
      via: "file read at runtime"
      pattern: "Path.*guidelines.*GUIDELINES\\.md"
---

<objective>
Create GUIDELINES.md design standards document that the AI analyzer will use as reference during design review.

Purpose: This document is critical infrastructure - the backend analyzer service loads it and includes it in the LLM prompt context. The structure and specificity directly impact analysis quality.

Output: `backend/guidelines/GUIDELINES.md` - a markdown document with checklist-style, measurable criteria optimized for LLM consumption.
</objective>

<execution_context>
@~/.claude/get-shit-done/workflows/execute-plan.md
@~/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/2C-assets/2C-RESEARCH.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create guidelines directory and GUIDELINES.md</name>
  <files>backend/guidelines/GUIDELINES.md</files>
  <action>
Create the guidelines directory at `backend/guidelines/` and create GUIDELINES.md with the following structure based on the research template:

1. **Header and intro** - Brief explanation that this defines design standards for AI review

2. **## UI States** section with:
   - Required states table (Default, Hover, Focus, Pressed, Disabled) with visual treatment and timing
   - Conditional states table (Loading, Error, Empty, Selected) with when required
   - Examples of missing states the AI should flag

3. **## Accessibility** section with:
   - Color contrast table (WCAG 2.1 AA: 4.5:1 normal, 3:1 large, 3:1 non-text)
   - Touch targets requirements (44x44px best practice, 24x24px AA minimum)
   - Focus indicator requirements (2px outline, 3:1 contrast)
   - Labels and alt text requirements
   - Examples of accessibility gaps to flag

4. **## Design Tokens** section with:
   - Colors table (primary, secondary, error, warning, success, text colors, backgrounds)
   - Spacing scale table (4, 8, 16, 24, 32, 48, 64px with token names and usage)
   - Typography scale table (heading-1 through caption with size, weight, line-height)
   - Border radius scale table
   - Valid values statement and violation examples

5. **## Responsiveness** section with:
   - Required breakpoints table (Mobile 320-479, Tablet 768-1023, Desktop 1024+)
   - How AI detects responsive designs (frame naming, widths)
   - Layout expectations by breakpoint
   - Examples of responsiveness gaps to flag

6. **## Custom Rules** section with:
   - Placeholder comment for company-specific rules
   - Example format showing how to add rules

Use markdown tables for all structured data - LLMs parse tables more reliably than prose.
Include specific values (not "good contrast" but "4.5:1").
Keep examples actionable and specific.
  </action>
  <verify>
- File exists: `ls backend/guidelines/GUIDELINES.md`
- Contains all four category headers: `grep -c "^## " backend/guidelines/GUIDELINES.md` returns 5 (States, Accessibility, Tokens, Responsiveness, Custom)
- Contains specific contrast value: `grep "4.5:1" backend/guidelines/GUIDELINES.md`
- Contains specific touch target: `grep "44" backend/guidelines/GUIDELINES.md`
- Contains spacing scale values: `grep "spacing" backend/guidelines/GUIDELINES.md`
  </verify>
  <done>
GUIDELINES.md exists at backend/guidelines/GUIDELINES.md with:
- All four analysis category sections (UI States, Accessibility, Design Tokens, Responsiveness)
- Custom Rules placeholder section
- Measurable values (contrast ratios, pixel sizes, spacing scale)
- Table-based format for LLM parsing
- At least 150 lines of content
  </done>
</task>

</tasks>

<verification>
1. GUIDELINES.md exists at correct path
2. Document has proper markdown structure (headers, tables)
3. All four analysis categories are represented
4. Custom rules section exists for user extension
5. Values are specific and measurable (not vague prose)
</verification>

<success_criteria>
- GUIDELINES.md file exists at `backend/guidelines/GUIDELINES.md`
- Document covers: UI States, Accessibility, Design Tokens, Responsiveness
- Contains specific WCAG values (4.5:1 contrast, 44px targets)
- Contains design token tables (colors, spacing, typography)
- Contains breakpoint definitions (320px, 768px, 1024px)
- Custom rules section allows user additions
- Structure uses tables and checklists (not prose paragraphs)
</success_criteria>

<output>
After completion, create `.planning/phases/2C-assets/2C-01-SUMMARY.md`
</output>
