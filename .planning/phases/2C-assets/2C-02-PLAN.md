---
phase: 2C-assets
plan: 02
type: execute
wave: 1
depends_on: []
files_modified: []
autonomous: false

must_haves:
  truths:
    - "Test Figma design exists with intentional issues in all four categories"
    - "MISSING_STATES issues: Button with only default state (no hover/focus/disabled)"
    - "ACCESSIBILITY issues: Low contrast text (#999 on white), small touch target (<44px)"
    - "DESIGN_SYSTEM issues: Off-scale spacing (15px), off-palette color"
    - "RESPONSIVENESS issues: Desktop-only frame with no mobile variant"
  artifacts:
    - path: "Figma file (cloud)"
      provides: "Test designs for demo and integration testing"
      contains: "Button-Default, Card-Desktop, Input-Default frames"
  key_links:
    - from: "Figma test designs"
      to: "Plugin selection"
      via: "Designer selects frames in Figma"
      pattern: "manual selection"
---

<objective>
Create sample Figma designs with intentional issues that demonstrate the design reviewer's capabilities across all four analysis categories.

Purpose: These test designs are essential for demo and integration testing. Each design must have obvious, intentional violations that the AI analyzer will detect - proving the tool's value.

Output: Figma file with 3 test component frames containing issues in: missing states, accessibility, design system, and responsiveness.
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

<task type="checkpoint:human-action" gate="blocking">
  <name>Task 1: Create test Figma designs with intentional issues</name>
  <action>
Designer creates a Figma file with test components. This cannot be automated - requires manual Figma design work.

**File Organization:**
```
Test Designs (Figma File)
  Page: Test Components
    Frame: Button-Default
    Frame: Card-Desktop
    Frame: Input-Default
```

**Component 1: Button-Default**
Purpose: Demonstrate MISSING_STATES + ACCESSIBILITY detection

Create ONLY:
- Single frame named "Button-Default" (no hover, focus, pressed, disabled variants)
- Rectangle 100x36px (intentionally below 44px height for a11y)
- Text label "#999999" on white background (2.85:1 contrast - FAILS 4.5:1)
- Background color: #0066CC (this is correct, to not have all violations)

Expected findings:
- "Missing hover state"
- "Missing focus state"
- "Missing pressed state"
- "Missing disabled state"
- "Contrast ratio below 4.5:1 minimum"
- "Touch target below 44x44px"

**Component 2: Card-Desktop**
Purpose: Demonstrate DESIGN_SYSTEM + RESPONSIVENESS detection

Create:
- Single frame named "Card-Desktop" at 400x300px (1024px-ish context)
- 15px padding on all sides (off-scale - should be 16px)
- Border color: #1177CC (not in token palette)
- 6px border radius (off-scale - should be 4px or 8px)
- NO "Card-Mobile" counterpart (missing breakpoint)

Expected findings:
- "Spacing value 15px not on design system scale (use 16px)"
- "Color #1177CC not in defined palette"
- "Border radius 6px not on scale (use 4px or 8px)"
- "Missing mobile variant (Card-Mobile)"

**Component 3: Input-Default**
Purpose: Demonstrate ALL FOUR categories

Create:
- Single frame named "Input-Default" at 320x48px
- Input rectangle with placeholder text only (no visible label)
- Placeholder text: #AAAAAA on white (fails contrast)
- No focus indicator designed
- No error state variant
- 10px padding (off-scale)
- Only desktop width (no mobile variant)

Expected findings:
- "Form input missing visible label"
- "Missing focus state"
- "Missing error state"
- "Contrast ratio below 4.5:1"
- "Spacing value 10px not on scale"
- "Missing responsive variants"
  </action>
  <how-to-verify>
1. Open Figma file
2. Confirm "Test Components" page exists
3. Confirm three frames exist: Button-Default, Card-Desktop, Input-Default
4. Verify each has intentional issues as specified:
   - Button: small size, low contrast text, only default state
   - Card: off-scale spacing/radius, wrong color, no mobile
   - Input: no label, no focus/error states, low contrast placeholder
  </how-to-verify>
  <resume-signal>
Type "created" and share Figma file URL (optional), or describe any changes made to the specification.
  </resume-signal>
</task>

</tasks>

<verification>
1. Figma file exists with "Test Components" page
2. Three frames present: Button-Default, Card-Desktop, Input-Default
3. Each frame has intentional issues in its target categories
4. NO state variants exist (only default states)
5. Issues are obvious enough to be reliably detected by AI
</verification>

<success_criteria>
- Test Figma file created with three frames
- Button-Default has: missing states (hover/focus/pressed/disabled), small size, low contrast
- Card-Desktop has: off-scale spacing (15px), non-token color, no mobile variant
- Input-Default has: missing label, no focus/error states, off-scale spacing, desktop only
- All four analysis categories covered across the three components
- Designs ready for plugin testing in Phase 3
</success_criteria>

<output>
After completion, create `.planning/phases/2C-assets/2C-02-SUMMARY.md`
</output>
