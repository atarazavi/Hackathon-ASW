# Design Guidelines

Placeholder guidelines for the design review agent. Phase 2C will create the full document.

## UI States

Every interactive component should have these states defined:

- **Default** - Normal resting state
- **Hover** - Mouse over state (desktop)
- **Focus** - Keyboard focus state (accessibility)
- **Pressed/Active** - During interaction
- **Disabled** - When interaction is not available
- **Loading** - While async operation in progress
- **Error** - When operation fails
- **Empty** - When no data to display

## Accessibility

Follow WCAG 2.1 Level AA guidelines:

- **Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text (18px+ or 14px+ bold)
- **Labels**: All interactive elements must have accessible labels
- **Focus visible**: Focus state must be visually distinct
- **Touch targets**: Minimum 44x44px for touch interactions

## Design System

### Spacing Scale (4px grid)

Use consistent spacing values:
- `4px` - Tight spacing (within components)
- `8px` - Small spacing (between related items)
- `16px` - Medium spacing (between sections)
- `24px` - Large spacing (major sections)
- `32px` - Extra large spacing (page-level)

### Color Tokens

- Use semantic color tokens (e.g., `primary`, `error`, `success`)
- Avoid hardcoded hex values outside the color system
- Ensure consistent color usage across similar elements

### Typography

- Use defined type scale (don't mix arbitrary font sizes)
- Maintain consistent font weights
- Ensure proper heading hierarchy (h1 > h2 > h3)

## Responsiveness

### Common Breakpoints

- **320px** - Mobile (small)
- **375px** - Mobile (standard)
- **768px** - Tablet
- **1024px** - Desktop (small)
- **1440px** - Desktop (wide)

### Responsive Design Checks

- Components should adapt appropriately at different widths
- Touch targets should be larger on mobile
- Typography may scale down on smaller screens
- Layout should reflow (not just scale) for different devices
