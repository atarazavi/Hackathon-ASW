# Phase 2C: Assets - Research

**Researched:** 2026-01-21
**Domain:** Design Guidelines Documentation + Figma Test Designs
**Confidence:** HIGH

## Summary

Phase 2C creates two demo assets for the Frontend Design Reviewer: (1) a GUIDELINES.md document that the AI agent uses as reference standards, and (2) sample Figma designs with intentional issues that demonstrate the tool's capabilities across all four analysis categories.

GUIDELINES.md is critical infrastructure - the backend analyzer service loads it at `backend/guidelines/GUIDELINES.md` and includes it in the LLM prompt context. The document structure directly impacts analysis quality: checklist-style, measurable criteria outperform prose descriptions for LLM parsing. The user has indicated they want to customize this file with company-specific rules, so the template must include clear extension points.

For test designs, the strategy is creating simple components (button, card, form) with deliberate violations in each of the four categories: missing states, accessibility gaps, design system violations, and responsiveness issues. Each violation should be obvious enough to be caught reliably while demonstrating the tool's value.

**Primary recommendation:** Structure GUIDELINES.md with clear sections mapping to the four analysis categories, using specific measurable values (e.g., "4.5:1 contrast ratio", "44x44px touch target", "8px spacing grid") that the AI can directly compare against extracted design data. Create test designs with at least 2-3 intentional issues per analysis category.

## Standard Stack

This phase produces documentation and design assets - no code dependencies.

### Deliverables

| Asset | Format | Location | Consumed By |
|-------|--------|----------|-------------|
| GUIDELINES.md | Markdown | `backend/guidelines/GUIDELINES.md` | Backend analyzer service (via file read) |
| Test Figma Design | Figma file | Figma (cloud) | Plugin testing, demo presentation |

### Integration with Backend

Based on Phase 2A research and plans, the analyzer service loads guidelines like this:

```python
# backend/app/services/analyzer.py
GUIDELINES_PATH = Path(__file__).parent.parent.parent / "guidelines" / "GUIDELINES.md"

# In analyze_design():
guidelines = ""
if GUIDELINES_PATH.exists():
    guidelines = GUIDELINES_PATH.read_text()

# Override with request guidelines if provided
if design_data.guidelines:
    guidelines = design_data.guidelines
```

The plugin can also send custom guidelines in the request payload, but the default file path is `backend/guidelines/GUIDELINES.md`.

## Architecture Patterns

### GUIDELINES.md Structure

The document must be optimized for LLM consumption. Research shows that checklist-style formats with specific values produce more reliable AI analysis than prose.

**Recommended structure:**

```markdown
# Design Guidelines

## UI States
[Required states for interactive elements with visual treatment specs]

## Accessibility
[WCAG 2.1 AA thresholds with specific ratios and sizes]

## Design Tokens
[Color, spacing, typography values in tables]

## Responsiveness
[Breakpoint requirements with layout expectations]

## Custom Rules
[Placeholder for company-specific additions]
```

### Pattern 1: Checklist-Style Guidelines

**What:** Structure each section as checkable criteria, not descriptive prose.
**When to use:** Always - LLMs perform better with specific, enumerable requirements.
**Why:** The AI can systematically check each item; vague prose leads to vague findings.

```markdown
## UI States

Interactive elements MUST have the following states:

### Required States (all interactive elements)
| State | Required | Visual Treatment | Timing |
|-------|----------|------------------|--------|
| Default | Yes | Full opacity, brand colors | - |
| Hover | Yes | Darken/lighten 10-20% | 150-200ms delay |
| Focus | Yes | 2px outline, 3:1 contrast | 100-150ms |
| Pressed | Yes | Darken 20-30% | Immediate |
| Disabled | Yes | 50% opacity, ARIA-disabled | - |

### Conditional States
| State | When Required | Visual Treatment |
|-------|---------------|------------------|
| Loading | Async actions | Spinner or skeleton |
| Error | Form validation | Red border + message |
| Empty | Lists/containers | Illustration + CTA |
| Selected | Toggles/checkboxes | Filled indicator |
```

### Pattern 2: Measurable Accessibility Thresholds

**What:** Specify exact WCAG values for each accessibility check.
**When to use:** Always - vague guidance produces vague findings.
**Source:** WCAG 2.1 Level AA requirements.

```markdown
## Accessibility

### Color Contrast (WCAG 2.1 AA - SC 1.4.3)
| Element Type | Minimum Ratio | Notes |
|--------------|---------------|-------|
| Normal text (<18px or <14px bold) | 4.5:1 | 4.49:1 FAILS |
| Large text (>=18px or >=14px bold) | 3:1 | ~24px CSS or 19px bold |
| Non-text (icons, focus indicators) | 3:1 | SC 1.4.11 |

### Touch Targets (WCAG 2.2)
| Level | Minimum Size | Notes |
|-------|--------------|-------|
| AA (SC 2.5.8) | 24x24 CSS pixels | Minimum requirement |
| Best practice | 44x44 CSS pixels | Recommended for all platforms |
| Mobile apps | 48x48 CSS pixels | Android Material guideline |

### Focus Indicators
- Outline width: 2px minimum
- Outline contrast: 3:1 against background
- Must be visually distinct from hover state
- Must be visible on ALL focusable elements
```

### Pattern 3: Semantic Token Definitions

**What:** Define design tokens with semantic names, specific values, and usage context.
**When to use:** For design system violation detection.
**Format:** Tables for easy AI parsing.

```markdown
## Design Tokens

### Colors
| Token Name | Hex Value | Usage |
|------------|-----------|-------|
| primary | #0066CC | Primary actions, links |
| primary-hover | #0052A3 | Primary button hover |
| error | #D32F2F | Error states, validation |
| text-primary | #212121 | Main body text |
| text-secondary | #757575 | Secondary text, captions |
| background | #FFFFFF | Page background |

### Spacing Scale (4px base)
| Token | Value | Usage |
|-------|-------|-------|
| spacing-xs | 4px | Icon gaps, tight padding |
| spacing-sm | 8px | Compact element spacing |
| spacing-md | 16px | Default spacing |
| spacing-lg | 24px | Section padding |
| spacing-xl | 32px | Major section breaks |

### Valid Spacing Values
Only these spacing values are valid: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64px
Any other value (e.g., 10px, 15px, 22px) is a design system violation.
```

### Pattern 4: Breakpoint Requirements

**What:** Define expected breakpoints with layout change expectations.
**When to use:** For responsiveness gap detection.
**Source:** Common 2026 breakpoint conventions.

```markdown
## Responsiveness

### Required Breakpoints
| Breakpoint | Width Range | Required For |
|------------|-------------|--------------|
| Mobile | 320px - 479px | All layouts |
| Mobile Large | 480px - 767px | Complex layouts |
| Tablet | 768px - 1023px | All layouts |
| Desktop | 1024px - 1439px | All layouts |
| Large Desktop | 1440px+ | Optional |

### Responsive Detection
The agent detects responsive intent when:
- Multiple frames have similar names with size indicators (e.g., "Card-mobile", "Card-desktop")
- Multiple frames have different widths suggesting breakpoints
- Frame widths match common breakpoints (320, 375, 768, 1024, 1440)

### Layout Expectations by Breakpoint
| Element | Mobile (<768px) | Desktop (>=1024px) |
|---------|-----------------|---------------------|
| Navigation | Hamburger menu | Horizontal nav |
| Columns | 1 column | 2-4 columns |
| Touch targets | 48px minimum | 44px minimum |
```

### Anti-Patterns to Avoid

- **Vague guidance:** "Use appropriate contrast" instead of "4.5:1 minimum"
- **Prose over checklists:** Paragraphs the AI must parse vs. enumerable items
- **Missing thresholds:** "Elements should be accessible" without specific criteria
- **Generic recommendations:** "Follow best practices" without defining them
- **Inconsistent formatting:** Mixing styles makes AI parsing unreliable
- **Orphan rules:** Rules without clear categories don't map to finding types

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Accessibility standards | Custom rules | WCAG 2.1 AA thresholds | Industry standard, well-documented |
| UI state lists | Ad-hoc enumeration | NN/g five core states | Research-backed, comprehensive |
| Breakpoint values | Random widths | Standard breakpoints (320, 768, 1024, 1440) | Match real device sizes |
| Contrast requirements | Guessed ratios | WCAG specific ratios (4.5:1, 3:1) | Legal compliance standard |
| Touch target sizes | Arbitrary minimums | WCAG 2.2 (24px AA, 44px AAA) | Accessibility compliance |
| Spacing scale | Random values | 4px/8px base grid | Industry convention |

**Key insight:** Design guidelines codify established standards. Use authoritative sources (WCAG, Material Design, NN/g) rather than inventing rules.

## Common Pitfalls

### Pitfall 1: Guidelines Too Vague for LLM

**What goes wrong:** AI returns generic findings like "consider improving contrast" without specifics.
**Why it happens:** Guidelines use prose descriptions instead of measurable criteria.
**How to avoid:** Use specific values (4.5:1 not "good contrast"), tables not paragraphs.
**Warning signs:** AI findings that could apply to any design, lacking specificity.

### Pitfall 2: Test Designs Too Perfect

**What goes wrong:** Demo shows no findings - defeats the purpose.
**Why it happens:** Designer naturally creates polished designs without intentional issues.
**How to avoid:** Create explicit checklist of intentional violations before designing.
**Warning signs:** During testing, AI returns "No issues found."

### Pitfall 3: Test Designs Only Have One Category of Issues

**What goes wrong:** Demo only shows accessibility findings, not all four categories.
**Why it happens:** Easier to think of one type of violation.
**How to avoid:** Create test design matrix with at least 2 issues per category.
**Warning signs:** Demo only exercises one or two agent capabilities.

### Pitfall 4: Guidelines Don't Match Analysis Categories

**What goes wrong:** Agent looks for things not defined in guidelines, or guidelines define things agent can't detect.
**Why it happens:** Guidelines created without reference to agent capabilities.
**How to avoid:** Structure guidelines to match the four analysis categories exactly: MISSING_STATES, ACCESSIBILITY, DESIGN_SYSTEM, RESPONSIVENESS.
**Warning signs:** Mismatch between guideline sections and finding categories.

### Pitfall 5: Company Customization Breaks Format

**What goes wrong:** User customizes GUIDELINES.md and LLM can't parse it.
**Why it happens:** No clear structure or guidance for user additions.
**How to avoid:** Provide clear section markers, "add your rules here" placeholders, and format examples.
**Warning signs:** After user edits, AI returns parsing errors or misses custom rules.

### Pitfall 6: Inconsistent Units Between Guidelines and Plugin

**What goes wrong:** Guidelines say "44px" but plugin extracts values in different units.
**Why it happens:** Figma uses different measurement systems (points, CSS pixels).
**How to avoid:** Use CSS pixels consistently - Figma dimensions are already in CSS pixel equivalents.
**Warning signs:** Size comparisons don't match expected thresholds.

## Test Design Strategy

### Intentional Issue Matrix

Create test designs that trigger findings in all four categories:

| Category | Intentional Issue | Expected Finding |
|----------|-------------------|------------------|
| MISSING_STATES | Button with only default state | "Missing hover, focus, disabled states" |
| MISSING_STATES | Form submit without loading state | "No loading indicator for async action" |
| MISSING_STATES | List without empty state | "Missing empty state for data list" |
| ACCESSIBILITY | Light gray text #999 on white #FFF | "Contrast ratio 2.85:1 below 4.5:1" |
| ACCESSIBILITY | 32x32px touch target | "Touch target below 44x44px minimum" |
| ACCESSIBILITY | Input without visible label | "Form input missing associated label" |
| DESIGN_SYSTEM | Color #0055BB instead of #0066CC | "Color not in defined palette" |
| DESIGN_SYSTEM | 15px spacing (not on 8px grid) | "Spacing value not on design system scale" |
| DESIGN_SYSTEM | 15px font size | "Typography not on type scale" |
| RESPONSIVENESS | Desktop frame only (1440px) | "Missing mobile breakpoint" |
| RESPONSIVENESS | 768px and 1440px, no 320px | "No mobile viewport under 480px" |

### Recommended Test Design Components

For hackathon demo, create these minimal test designs:

**1. Button Component (states + accessibility)**
- **Missing states:** Only "Default" variant exists (no hover, focus, pressed, disabled)
- **A11y issues:** Light gray text (#999999), 36x36px size
- **Frame name:** "Button-Default"

**2. Card Component (design system + responsiveness)**
- **DS violations:** 15px padding (not on scale), color #1177CC (not a token)
- **Responsive issue:** Only 1024px width, no mobile variant
- **Frame names:** "Card-Desktop" (no "Card-Mobile" counterpart)

**3. Form Input (all categories)**
- **Missing states:** No error state, no disabled state, no focus indicator
- **A11y:** Label text too light, no focus visible
- **DS:** Inconsistent border radius, off-scale margins
- **Responsive:** Desktop width only
- **Frame name:** "Input-Default"

### Figma File Organization

```
Test Designs (Figma File)
├── Page: Test Components
│   ├── Frame: Button-Default (has issues - no other states)
│   ├── Frame: Card-Desktop (missing mobile variant)
│   └── Frame: Input-Default (multiple issues)
└── Page: Reference (Optional)
    ├── Frame: Button-AllStates (correct implementation)
    └── Frame: Card-Mobile + Card-Desktop (proper responsive)
```

**Note:** Test designs should be obviously flawed. The goal is demonstrating detection, not subtle edge cases.

## Code Examples

### Complete GUIDELINES.md Template

```markdown
# Design Guidelines

This document defines design standards for the AI reviewer.
Edit the values below to match your company's design system.

---

## UI States

Interactive elements MUST have the following states designed:

### Required States (All Interactive Elements)
| State | Required | Visual Treatment | Timing |
|-------|----------|------------------|--------|
| Default | Yes | Full opacity, brand colors | - |
| Hover | Yes | Darken/lighten by 10-20% | 150-200ms delay |
| Focus | Yes | 2px outline, 3:1 contrast | 100-150ms |
| Pressed | Yes | Darken by 20-30% | Immediate |
| Disabled | Yes | 50% opacity, ARIA-disabled | - |

### Conditional States
| State | When Required | Visual Treatment |
|-------|---------------|------------------|
| Loading | Async actions (submit, fetch) | Spinner or skeleton |
| Error | Form validation, API errors | Red border + error message |
| Empty | Lists, tables, search results | Illustration + call to action |
| Selected | Toggles, checkboxes, tabs | Filled indicator or highlight |

### Examples of Missing States (what the AI should flag)
- Button without hover effect
- Input without error state
- List without empty state
- Toggle without selected state
- Form submit without loading state

---

## Accessibility

### Color Contrast (WCAG 2.1 AA)
| Element Type | Minimum Ratio |
|--------------|---------------|
| Normal text (<18px) | 4.5:1 |
| Large text (>=18px or >=14px bold) | 3:1 |
| Non-text (icons, borders, focus) | 3:1 |

### Touch Targets
- Minimum size: 44 x 44 CSS pixels (best practice)
- WCAG 2.2 AA minimum: 24 x 24 CSS pixels
- Mobile recommended: 48 x 48 CSS pixels
- Minimum spacing between targets: 8 pixels

### Focus Indicators
- Outline width: 2px minimum
- Outline contrast: 3:1 against background
- Must be visible on all focusable elements
- Must be visually distinct from hover state

### Labels and Alt Text
- All form inputs must have visible labels
- All images must have alt text (or empty alt for decorative)
- All icon-only buttons must have aria-label

### Examples of Accessibility Gaps (what the AI should flag)
- Gray text (#999999) on white background (2.85:1 ratio - FAIL)
- 32x32px button (below 44px minimum)
- Focus state identical to hover state
- Input with placeholder only, no label

---

## Design Tokens

### Colors
<!-- Edit these values to match your design system -->
| Token Name | Hex Value | Usage |
|------------|-----------|-------|
| primary | #0066CC | Primary actions, links |
| primary-hover | #0052A3 | Primary hover state |
| secondary | #6C757D | Secondary actions |
| error | #D32F2F | Error states, validation |
| warning | #ED6C02 | Warning states |
| success | #2E7D32 | Success states |
| text-primary | #212121 | Main body text |
| text-secondary | #757575 | Secondary text |
| background | #FFFFFF | Page background |
| surface | #F5F5F5 | Card backgrounds |

### Spacing Scale
<!-- Edit these values to match your design system -->
| Token | Value | Usage |
|-------|-------|-------|
| spacing-xs | 4px | Icon gaps, tight padding |
| spacing-sm | 8px | Compact spacing |
| spacing-md | 16px | Default spacing |
| spacing-lg | 24px | Section padding |
| spacing-xl | 32px | Major sections |
| spacing-xxl | 48px | Page-level spacing |

**Valid spacing values:** 4, 8, 16, 24, 32, 48, 64px
Any other value is a design system violation.

### Typography Scale
| Token | Size | Weight | Line Height |
|-------|------|--------|-------------|
| heading-1 | 32px | 700 | 1.2 |
| heading-2 | 24px | 600 | 1.3 |
| heading-3 | 20px | 600 | 1.4 |
| body-lg | 18px | 400 | 1.5 |
| body | 16px | 400 | 1.5 |
| body-sm | 14px | 400 | 1.4 |
| caption | 12px | 400 | 1.4 |

### Border Radius Scale
| Token | Value | Usage |
|-------|-------|-------|
| radius-sm | 4px | Buttons, inputs |
| radius-md | 8px | Cards, modals |
| radius-lg | 16px | Large containers |
| radius-full | 9999px | Pills, avatars |

### Examples of Design System Violations (what the AI should flag)
- Using #0055BB instead of #0066CC (primary)
- Using 12px spacing (not on 4/8/16/24 scale)
- Using 15px font size (not on typography scale)
- Using 6px border radius (not on radius scale)

---

## Responsiveness

### Required Breakpoints
| Breakpoint | Width Range | Required For |
|------------|-------------|--------------|
| Mobile | 320px - 479px | All layouts |
| Tablet | 768px - 1023px | All layouts |
| Desktop | 1024px+ | All layouts |

### How the AI Detects Responsive Designs
The agent looks for:
- Multiple frames with similar names and size indicators ("Card-mobile", "Card-desktop")
- Frame widths matching common breakpoints (320, 375, 768, 1024, 1440)
- Missing size variants when responsive intent is detected

### Layout Expectations
| Element | Mobile (<768px) | Desktop (>=1024px) |
|---------|-----------------|---------------------|
| Navigation | Hamburger/drawer | Horizontal |
| Columns | 1 | 2-4 |
| Touch targets | 48px | 44px |

### Examples of Responsiveness Gaps (what the AI should flag)
- Desktop-only design (1440px) with no mobile variant
- "Card-desktop" frame exists but no "Card-mobile"
- Only 768px breakpoint, missing mobile (320px)

---

## Custom Rules

<!-- ADD YOUR COMPANY-SPECIFIC RULES BELOW -->

### [Your Category Name]
Add additional rules your team wants to enforce.

Example format:
| Rule | Requirement | Violation Example |
|------|-------------|-------------------|
| Brand color usage | Only use approved brand colors | Using #FF0000 instead of brand red |

---

*Last updated: [DATE]*
*Based on: WCAG 2.1 AA, NN/g research, [your design system name]*
```

## State of the Art

| Old Approach | Current Approach | Impact |
|--------------|------------------|--------|
| Prose-based design specs | Checklist + table guidelines | LLMs extract requirements reliably |
| Manual design QA | AI-powered design review | Faster, consistent, scalable |
| Fixed company guidelines | Customizable templates | Reusable across organizations |
| Single-device mockups | Multi-breakpoint responsive | Standard expectation |
| "Looks good" contrast | WCAG ratio measurements | Objective, legally compliant |
| Arbitrary touch targets | WCAG 2.2 standards (24/44px) | Accessibility compliance |

**Key insight:** WCAG 2.2 (current) has updated touch target requirements: Level AA is 24x24px minimum, but 44x44px remains best practice and Level AAA requirement.

## Open Questions

### 1. Guidelines File Format Evolution

**What we know:** Backend loads GUIDELINES.md as plain text into the LLM prompt.
**What's unclear:** Whether YAML frontmatter or JSON sections would improve AI parsing.
**Recommendation:** Start with pure markdown tables. If AI struggles, add structured metadata later. Keep it simple for hackathon.

### 2. Company Customization Workflow

**What we know:** User wants to customize with company rules.
**What's unclear:** How sophisticated the customization UI needs to be.
**Recommendation:** For hackathon, support direct file editing with clear comments. Future: Plugin could have a guidelines editor panel.

### 3. Token Value Extraction from Plugin

**What we know:** Plugin extracts colors as hex values, spacing as pixels.
**What's unclear:** Exact precision of extracted values (rounding, etc.).
**Recommendation:** Guidelines should use CSS pixel values to match Figma's coordinate system. Colors as hex (#RRGGBB).

## Sources

### Primary (HIGH confidence)
- [WCAG 2.1 Contrast Requirements](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) - Official W3C contrast specifications (4.5:1, 3:1)
- [WCAG 2.2 Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) - Touch target requirements (24x24px AA, 44x44px AAA)
- [NN/g Button States](https://www.nngroup.com/articles/button-states-communicate-interaction/) - Five core button states: enabled, disabled, hover, focus, pressed

### Secondary (MEDIUM confidence)
- [UXPin Design System Documentation](https://www.uxpin.com/studio/blog/design-system-documentation-guide/) - Documentation structure best practices
- [BrowserStack Responsive Breakpoints](https://www.browserstack.com/guide/responsive-design-breakpoints) - 2026 breakpoint conventions
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) - Contrast ratio verification
- [LogRocket Button States](https://blog.logrocket.com/ux-design/designing-button-states/) - Comprehensive state design patterns

### Tertiary (LOW confidence)
- [Figma Design QA Checklist](https://www.figma.com/community/file/1487501775359145058/design-qa-checklist) - Community template (general reference)

## Metadata

**Confidence breakdown:**
- Guidelines structure: HIGH - based on WCAG, NN/g authoritative sources
- Accessibility thresholds: HIGH - WCAG 2.1/2.2 is definitive standard
- UI states list: HIGH - NN/g research is authoritative
- Design token format: HIGH - follows established conventions
- Test design strategy: MEDIUM - logical approach, needs validation during demo
- Breakpoint values: MEDIUM - industry conventions, no single standard

**Research date:** 2026-01-21
**Valid until:** 2026-04-21 (90 days - stable domain, standards don't change frequently)
