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

| Element Type | Minimum Ratio | Notes |
|--------------|---------------|-------|
| Normal text (<18px or <14px bold) | 4.5:1 | 4.49:1 FAILS |
| Large text (>=18px or >=14px bold) | 3:1 | ~24px CSS or 19px bold |
| Non-text (icons, focus indicators) | 3:1 | SC 1.4.11 |

### Touch Targets

| Level | Minimum Size | Notes |
|-------|--------------|-------|
| Best practice | 44x44 CSS pixels | Recommended for all platforms |
| WCAG 2.2 AA (SC 2.5.8) | 24x24 CSS pixels | Minimum requirement |
| Mobile apps | 48x48 CSS pixels | Android Material guideline |

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
| spacing-sm | 8px | Compact element spacing |
| spacing-md | 16px | Default spacing |
| spacing-lg | 24px | Section padding |
| spacing-xl | 32px | Major section breaks |
| spacing-xxl | 48px | Page-level spacing |
| spacing-xxxl | 64px | Large page sections |

**Valid spacing values:** 4, 8, 16, 24, 32, 48, 64px
Any other value (e.g., 10px, 15px, 22px) is a design system violation.

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
| Mobile Large | 480px - 767px | Complex layouts |
| Tablet | 768px - 1023px | All layouts |
| Desktop | 1024px+ | All layouts |

### How the AI Detects Responsive Designs

The agent looks for:
- Multiple frames with similar names and size indicators ("Card-mobile", "Card-desktop")
- Frame widths matching common breakpoints (320, 375, 768, 1024, 1440)
- Missing size variants when responsive intent is detected

### Layout Expectations by Breakpoint

| Element | Mobile (<768px) | Desktop (>=1024px) |
|---------|-----------------|---------------------|
| Navigation | Hamburger menu/drawer | Horizontal nav bar |
| Columns | 1 column | 2-4 columns |
| Touch targets | 48px minimum | 44px minimum |
| Font sizes | May scale down | Full size |

### Examples of Responsiveness Gaps (what the AI should flag)

- Desktop-only design (1440px) with no mobile variant
- "Card-desktop" frame exists but no "Card-mobile"
- Only 768px breakpoint, missing mobile (320px)
- Navigation visible at mobile width without mobile adaptation

---

## Custom Rules

<!-- ADD YOUR COMPANY-SPECIFIC RULES BELOW -->

### [Your Category Name]

Add additional rules your team wants to enforce.

Example format:

| Rule | Requirement | Violation Example |
|------|-------------|-------------------|
| Brand color usage | Only use approved brand colors | Using #FF0000 instead of brand red |
| Logo spacing | Maintain 24px clearance around logo | Logo touching other elements |
| Button height | All buttons must be 40px tall | 32px button |

---

*Last updated: 2026-01-21*
*Based on: WCAG 2.1 AA, WCAG 2.2 Touch Targets, NN/g UI State Research*
