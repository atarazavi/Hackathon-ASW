# Phase 2C: Assets - Research

**Researched:** 2026-01-21
**Domain:** Design Guidelines Documentation + Figma Test Designs
**Confidence:** HIGH

## Summary

This phase creates demo materials for the Frontend Design Reviewer: a GUIDELINES.md document that the AI agent uses as reference standards, and sample Figma designs with intentional issues that trigger findings across all four analysis categories (missing states, accessibility, design system, responsiveness).

The core insight is that GUIDELINES.md serves dual purposes: (1) it defines the "rules" the AI compares against, and (2) it provides context for generating actionable recommendations. The document should be structured as a checklist-style reference with specific, measurable criteria rather than prose. This makes LLM analysis more reliable and findings more actionable.

For test designs, the strategy is to create a small component (e.g., a button or card) with deliberate violations that demonstrate the tool's capabilities. Each violation should be obvious enough to be caught reliably, covering all four categories the agent analyzes.

**Primary recommendation:** Structure GUIDELINES.md with clear sections for each analysis category, using specific values (e.g., "4.5:1 contrast ratio", "44x44px touch target") that the AI can directly compare against extracted design data. Create test designs with at least one intentional issue per analysis category.

## Standard Stack

This phase is documentation and design work - no code dependencies.

### Deliverables

| Asset | Format | Purpose | Consumed By |
|-------|--------|---------|-------------|
| GUIDELINES.md | Markdown | Design standards for agent reference | Backend analyzer service |
| Test Figma Design | Figma file | Demo designs with intentional issues | Plugin testing, demo presentation |

### File Location

Based on Phase 2A research, the backend expects guidelines at:
```
backend/guidelines/GUIDELINES.md
```

The analyzer service loads this file and includes it in the LLM prompt context. This path is configurable - the plugin can also send custom guidelines in the request payload.

## Architecture Patterns

### GUIDELINES.md Structure

Based on research into design system documentation best practices, the guidelines document should be structured for LLM consumption, not human reading. Key principles:

1. **Checklist-style, not prose** - Specific criteria the AI can check
2. **Measurable values** - Numbers, not descriptions ("4.5:1" not "good contrast")
3. **Organized by analysis category** - Matches the four agent detection categories
4. **Examples of violations** - Helps AI recognize patterns

**Recommended structure:**

```markdown
# Design Guidelines

## UI States
[Required states for interactive elements]

## Accessibility
[WCAG requirements and thresholds]

## Design Tokens
[Color, spacing, typography values]

## Responsiveness
[Breakpoint requirements]
```

### Pattern 1: Checklist-Style Guidelines

**What:** Structure each section as checkable criteria, not descriptive prose.
**When to use:** Always - LLMs perform better with specific, enumerable requirements.

```markdown
## UI States

Interactive elements MUST have the following states:

### Required States (all interactive elements)
- [ ] Default/Enabled - Normal state
- [ ] Hover - Mouse-over feedback (150-200ms delay)
- [ ] Focus - Keyboard navigation indicator (visible outline)
- [ ] Pressed/Active - Click/tap feedback (within 100-150ms)
- [ ] Disabled - Unavailable state (50% opacity, ARIA-disabled)

### Conditional States (context-dependent)
- [ ] Loading - In-progress indicator (for async actions)
- [ ] Error - Validation failure state
- [ ] Empty - No content state (for containers/lists)
- [ ] Selected - Toggle/checkbox states
```

### Pattern 2: Measurable Accessibility Thresholds

**What:** Specify exact WCAG values for each accessibility check.
**When to use:** Always - vague guidance produces vague findings.

```markdown
## Accessibility

### Color Contrast (WCAG 2.1 AA)
- Normal text (<18px or <14px bold): 4.5:1 minimum ratio
- Large text (>=18px or >=14px bold): 3:1 minimum ratio
- Non-text elements (icons, focus indicators): 3:1 minimum ratio

### Touch Targets
- Minimum size: 44x44 CSS pixels (48x48 recommended)
- Minimum spacing between targets: 8px

### Focus Indicators
- Visible outline: 2px solid minimum
- Contrast against background: 3:1 minimum ratio
- Must be distinct from hover state
```

### Pattern 3: Semantic Token Definitions

**What:** Define design tokens with semantic names and values.
**When to use:** For design system violation detection.

```markdown
## Design Tokens

### Colors
| Token | Value | Usage |
|-------|-------|-------|
| primary | #0066CC | Primary actions, links |
| primary-hover | #0052A3 | Primary hover state |
| error | #D32F2F | Error states, validation |
| text-primary | #212121 | Main text |
| text-secondary | #757575 | Secondary text |
| background | #FFFFFF | Page background |

### Spacing Scale
| Token | Value | Usage |
|-------|-------|-------|
| spacing-xs | 4px | Tight spacing |
| spacing-sm | 8px | Compact spacing |
| spacing-md | 16px | Default spacing |
| spacing-lg | 24px | Section spacing |
| spacing-xl | 32px | Large sections |
```

### Pattern 4: Breakpoint Requirements

**What:** Define expected breakpoints and what changes at each.
**When to use:** For responsiveness gap detection.

```markdown
## Responsiveness

### Required Breakpoints
| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Mobile | 320px | Single column, stacked navigation |
| Tablet | 768px | Two columns, collapsed sidebar |
| Desktop | 1024px | Full layout, horizontal navigation |
| Large Desktop | 1440px | Maximum content width |

### Detection Heuristics
When multiple frames are selected:
- Similar names with size suffixes (e.g., "Card-mobile", "Card-desktop") indicate responsive variants
- Different widths (320, 768, 1024, 1440) suggest breakpoint coverage
- Missing intermediate size triggers "responsiveness gap" finding
```

### Anti-Patterns to Avoid

- **Vague guidance:** "Use appropriate contrast" instead of "4.5:1 minimum"
- **Prose over checklists:** Paragraphs the AI must parse vs. enumerable items
- **Missing thresholds:** "Elements should be accessible" without specific criteria
- **Generic recommendations:** "Follow best practices" without defining them
- **Inconsistent formatting:** Mixing styles makes AI parsing unreliable

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Accessibility standards | Custom rules | WCAG 2.1 AA thresholds | Industry standard, well-documented |
| UI state lists | Ad-hoc enumeration | Material Design / NN/g state lists | Comprehensive, research-backed |
| Breakpoint values | Random widths | Bootstrap/Tailwind standard breakpoints | Match common device sizes |
| Contrast requirements | Guessed ratios | WCAG 2.1 specific ratios (4.5:1, 3:1) | Legal compliance standard |

**Key insight:** Design guidelines are not novel - they codify established standards. Use authoritative sources (WCAG, Material Design, established design systems) rather than inventing rules.

## Common Pitfalls

### Pitfall 1: Guidelines Too Vague for LLM

**What goes wrong:** AI returns generic findings like "consider improving contrast" without specifics.
**Why it happens:** Guidelines use prose descriptions instead of measurable criteria.
**How to avoid:** Use specific values (4.5:1 not "good contrast"), checklists not paragraphs.
**Warning signs:** AI findings that could apply to any design, lacking specificity.

### Pitfall 2: Test Designs Too Perfect

**What goes wrong:** Demo shows no findings - defeats the purpose.
**Why it happens:** Designer naturally creates polished designs without intentional issues.
**How to avoid:** Create explicit checklist of intentional violations before designing.
**Warning signs:** During testing, AI returns "No issues found."

### Pitfall 3: Test Designs Only Have One Category of Issues

**What goes wrong:** Demo only shows accessibility findings, not all four categories.
**Why it happens:** Easier to think of one type of violation.
**How to avoid:** Create test design matrix with at least one issue per category.
**Warning signs:** Demo only exercises one or two agent capabilities.

### Pitfall 4: Guidelines Don't Match Analysis Categories

**What goes wrong:** Agent looks for things not defined in guidelines, or guidelines define things agent can't detect.
**Why it happens:** Guidelines created without reference to agent capabilities.
**How to avoid:** Structure guidelines to match the four analysis categories exactly: MISSING_STATES, ACCESSIBILITY, DESIGN_SYSTEM, RESPONSIVENESS.
**Warning signs:** Mismatch between guideline sections and finding categories.

### Pitfall 5: Company Customization Breaks Format

**What goes wrong:** User customizes GUIDELINES.md and LLM can't parse it.
**Why it happens:** No clear structure for user additions.
**How to avoid:** Provide clear section markers and "add your rules here" placeholders.
**Warning signs:** After user edits, AI returns parsing errors or misses custom rules.

## Test Design Strategy

### Intentional Issue Matrix

Create test designs that trigger findings in all four categories:

| Category | Intentional Issue | Expected Finding |
|----------|-------------------|------------------|
| MISSING_STATES | Button with no hover/disabled state | "Missing hover state on Button" |
| MISSING_STATES | Form without loading state | "No loading indicator for async action" |
| ACCESSIBILITY | Light gray text on white (#999 on #FFF) | "Contrast ratio 2.8:1 below 4.5:1 requirement" |
| ACCESSIBILITY | 30x30px touch target | "Touch target below 44x44px minimum" |
| DESIGN_SYSTEM | Using #0055BB instead of token #0066CC | "Color #0055BB not in defined palette" |
| DESIGN_SYSTEM | 12px spacing (not on scale) | "Spacing 12px not on scale (8px, 16px, 24px)" |
| RESPONSIVENESS | Desktop frame only, no mobile | "Missing mobile breakpoint (320px)" |
| RESPONSIVENESS | 768px and 1440px, no 320px | "No mobile viewport under 480px" |

### Recommended Test Design Components

For a hackathon demo, create these minimal test designs:

1. **Button Component** (states + accessibility)
   - Missing: hover, focus, disabled states
   - A11y: Low contrast text, small touch target

2. **Card Component** (design system + responsiveness)
   - DS: Off-scale spacing, non-token colors
   - Responsive: Only desktop size, no mobile version

3. **Form Component** (all categories)
   - States: Missing loading, error, empty states
   - A11y: Missing labels, low contrast
   - DS: Inconsistent spacing
   - Responsive: Desktop only

### Figma File Organization

Recommended structure for test designs:

```
Test Designs (Figma File)
├── Page: Test Components
│   ├── Frame: Button-Default (has issues)
│   ├── Frame: Button-Fixed (reference)
│   ├── Frame: Card-Desktop (missing mobile)
│   └── Frame: Card-Mobile (fixed version)
└── Page: Demo Flow
    ├── Frame: Before (with issues)
    └── Frame: After (fixed)
```

## Code Examples

### Complete GUIDELINES.md Template

```markdown
# Design Guidelines

This document defines the design standards that the AI agent uses to review designs.
Edit the values below to match your company's design system.

## UI States

Interactive elements MUST have the following states designed:

### Required States (All Interactive Elements)
| State | Required | Visual Treatment |
|-------|----------|------------------|
| Default/Enabled | Yes | Full opacity, brand colors |
| Hover | Yes | Darkened/lightened by 10-20% |
| Focus | Yes | 2px outline, 3:1 contrast |
| Pressed/Active | Yes | Darkened by 20-30% |
| Disabled | Yes | 50% opacity, non-interactive cursor |

### Conditional States
| State | When Required | Visual Treatment |
|-------|---------------|------------------|
| Loading | Async actions | Spinner or skeleton |
| Error | Form validation | Red border, error message |
| Empty | Lists/containers | Illustration + call to action |
| Selected | Toggles/checkboxes | Filled indicator |

**Examples of missing states:**
- Button without hover effect
- Input without error state
- List without empty state
- Toggle without selected state

---

## Accessibility

### Color Contrast (WCAG 2.1 AA)
| Element Type | Minimum Ratio |
|--------------|---------------|
| Normal text (<18px) | 4.5:1 |
| Large text (>=18px or >=14px bold) | 3:1 |
| Non-text (icons, borders, focus) | 3:1 |

### Touch Targets
- Minimum size: 44 x 44 CSS pixels
- Recommended size: 48 x 48 CSS pixels
- Minimum spacing between targets: 8 pixels

### Focus Indicators
- Outline width: 2px minimum
- Outline contrast: 3:1 against background
- Must be visible on all focusable elements

### Labels and Alt Text
- All inputs must have associated labels
- All images must have alt text (or empty alt for decorative)
- All icons must have aria-label if standalone

**Examples of accessibility gaps:**
- Gray text (#999) on white background (2.8:1 ratio)
- 32x32px button (below 44px minimum)
- Focus state same as hover state
- Input without label element

---

## Design Tokens

### Colors
<!-- Edit these values to match your design system -->
| Token Name | Hex Value | Usage |
|------------|-----------|-------|
| primary | #0066CC | Primary actions, links |
| primary-hover | #0052A3 | Primary button hover |
| secondary | #6C757D | Secondary actions |
| error | #D32F2F | Error states, validation |
| warning | #ED6C02 | Warning states |
| success | #2E7D32 | Success states |
| text-primary | #212121 | Main body text |
| text-secondary | #757575 | Secondary text, captions |
| background | #FFFFFF | Page background |
| surface | #F5F5F5 | Card/elevated backgrounds |

### Spacing Scale
<!-- Edit these values to match your design system -->
| Token | Value | Usage |
|-------|-------|-------|
| spacing-xs | 4px | Icon gaps, tight padding |
| spacing-sm | 8px | Compact element spacing |
| spacing-md | 16px | Default spacing |
| spacing-lg | 24px | Section padding |
| spacing-xl | 32px | Major section breaks |
| spacing-xxl | 48px | Page-level spacing |

### Typography
| Token | Size | Weight | Line Height |
|-------|------|--------|-------------|
| heading-1 | 32px | 700 | 1.2 |
| heading-2 | 24px | 600 | 1.3 |
| heading-3 | 20px | 600 | 1.4 |
| body-lg | 18px | 400 | 1.5 |
| body | 16px | 400 | 1.5 |
| body-sm | 14px | 400 | 1.4 |
| caption | 12px | 400 | 1.4 |

### Border Radius
| Token | Value | Usage |
|-------|-------|-------|
| radius-none | 0px | Sharp corners |
| radius-sm | 4px | Buttons, inputs |
| radius-md | 8px | Cards, modals |
| radius-lg | 16px | Large containers |
| radius-full | 9999px | Pills, avatars |

**Examples of design system violations:**
- Using #0055BB instead of #0066CC (primary)
- Using 12px spacing (not on 4/8/16/24 scale)
- Using 15px font size (not on scale)
- Using 6px border radius (not on scale)

---

## Responsiveness

### Required Breakpoints
| Breakpoint | Width | Required For |
|------------|-------|--------------|
| Mobile | 320px - 479px | All layouts |
| Mobile Large | 480px - 767px | Complex layouts |
| Tablet | 768px - 1023px | All layouts |
| Desktop | 1024px - 1439px | All layouts |
| Large Desktop | 1440px+ | Optional |

### Breakpoint Detection
The agent detects responsive intent when:
- Multiple frames have similar names with size indicators ("mobile", "tablet", "desktop")
- Multiple frames have different widths suggesting breakpoints
- Frame widths match common breakpoints (320, 768, 1024, 1440)

### Layout Changes by Breakpoint
| Element | Mobile | Tablet | Desktop |
|---------|--------|--------|---------|
| Navigation | Hamburger | Hamburger | Horizontal |
| Columns | 1 | 2 | 3+ |
| Sidebar | Hidden | Collapsed | Visible |
| Touch targets | 48px | 44px | 44px |

**Examples of responsiveness gaps:**
- Desktop-only design (1440px) with no mobile variant
- Missing tablet breakpoint when mobile and desktop exist
- Component designed at 768px only (no mobile)

---

## Custom Rules

<!-- Add your company-specific rules below -->

### [Your Category]
Add additional rules your team wants to enforce.

---

*Last updated: [DATE]*
*Based on: WCAG 2.1 AA, Material Design guidelines, company design system v[X]*
```

## State of the Art

| Old Approach | Current Approach | Impact |
|--------------|------------------|--------|
| Prose-based design specs | Checklist-based guidelines | LLMs extract requirements more reliably |
| Manual design QA | AI-powered design review | Faster, consistent checking |
| Fixed guidelines documents | Company-customizable templates | Reusable across organizations |
| Single-device designs | Multi-breakpoint responsive | Expected standard for all new designs |
| Contrast "looks fine" | WCAG ratio measurements | Objective, accessible compliance |

**Current best practice:** Design guidelines should be structured data (tables, checklists) rather than prose. This enables both human comprehension and machine parsing.

## Open Questions

### 1. Guidelines File Format

**What we know:** Backend loads GUIDELINES.md and includes in prompt.
**What's unclear:** Optimal format for LLM parsing - pure markdown vs. structured YAML frontmatter.
**Recommendation:** Start with markdown tables and lists. If AI struggles to parse, consider adding YAML metadata.

### 2. Company Customization Workflow

**What we know:** User wants to customize with company rules.
**What's unclear:** How users will edit - direct file edit, plugin UI, or separate config?
**Recommendation:** For hackathon, support direct file edit with clear section markers. Future: Plugin could send custom guidelines in request.

### 3. Token Extraction from Design Data

**What we know:** Plugin extracts colors, spacing from Figma.
**What's unclear:** Exact format of extracted values (hex, rgba, px, rem).
**Recommendation:** Guidelines should define tokens in same format plugin extracts (likely hex for colors, px for spacing).

## Sources

### Primary (HIGH confidence)
- [NN/g Button States](https://www.nngroup.com/articles/button-states-communicate-interaction/) - Five core button states and visual treatments
- [U.S. Web Design System Design Tokens](https://designsystem.digital.gov/design-tokens/) - Token categories and naming conventions
- [WCAG 2.1 Level AA](https://wcag.dock.codes/documentation/wcag21aa/) - Official accessibility requirements
- [WebAIM Contrast and Color](https://webaim.org/articles/contrast/) - WCAG contrast ratio specifics

### Secondary (MEDIUM confidence)
- [UXPin Design System Documentation](https://www.uxpin.com/studio/blog/design-system-documentation-guide/) - Documentation structure best practices
- [BrowserStack Responsive Breakpoints](https://www.browserstack.com/guide/responsive-design-breakpoints) - Standard breakpoint values
- [Supernova Accessibility in Design Systems](https://www.supernova.io/blog/accessibility-in-design-systems-a-comprehensive-approach-through-documentation-and-assets) - A11y documentation patterns
- [LogRocket Button States](https://blog.logrocket.com/ux-design/designing-button-states/) - Interaction state design patterns

### Tertiary (LOW confidence)
- [Figma Design QA Checklist Community File](https://www.figma.com/community/file/1487501775359145058/design-qa-checklist) - Community template (unable to verify specific contents)
- [Medium Design Tokens Articles](https://medium.com/@wicar/streamlining-your-design-system-a-guide-to-tokens-and-naming-conventions-3e4553aa8821) - Token naming conventions

## Metadata

**Confidence breakdown:**
- Guidelines structure: HIGH - based on authoritative WCAG, NN/g, USWDS sources
- Accessibility thresholds: HIGH - WCAG 2.1 AA is definitive standard
- UI states list: HIGH - NN/g and Material Design are authoritative
- Test design strategy: MEDIUM - logical approach, needs validation during implementation
- Breakpoint values: MEDIUM - industry conventions but no single standard

**Research date:** 2026-01-21
**Valid until:** 2026-04-21 (90 days - stable domain, guidelines don't change frequently)
