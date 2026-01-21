# Feature Landscape: Frontend Accelerator MCP Tools

**Domain:** AI-powered design-to-code workflow for Angular
**Researched:** 2026-01-21
**Confidence:** HIGH (based on official MCP spec, Figma/Jira official docs, existing MCP implementations)

## Executive Summary

For a 3-4 hour hackathon, the key insight is: **existing MCP servers already solve Jira and Figma access**. Your value-add is the **agent orchestration layer** that combines these data sources and produces Angular output.

Recommended approach:
1. Use existing tools where possible (Figma MCP, Atlassian MCP, Angular CLI MCP)
2. Build custom tools only for your unique value: ticket analysis, design gap detection, and Angular generation
3. Create one composite "accelerate" tool that chains the full workflow

---

## Table Stakes (Must Have for Demo)

Features the demo absolutely needs to show the core value proposition.

| Tool | Purpose | Complexity | Input | Output |
|------|---------|------------|-------|--------|
| `analyze_ticket` | Fetch Jira ticket and extract structured requirements | Medium | `ticket_id: string` | Requirements object with user stories, ACs, linked designs |
| `analyze_design` | Fetch Figma design and identify implementation details | Medium | `figma_url: string` | Component structure, states, tokens, gaps |
| `generate_component` | Generate Angular component matching workspace patterns | High | `spec: object, context: object` | Angular component files (ts, html, scss, spec) |
| `accelerate` | End-to-end: ticket ID to generated component | High | `ticket_id: string` | Complete analysis + generated code |

### Tool Signatures

```typescript
// Core workflow tool - the demo money shot
interface AccelerateTool {
  name: "accelerate";
  description: "Generate an Angular component from a Jira ticket. Fetches ticket details, extracts linked Figma designs, analyzes requirements, and produces implementation-ready code.";
  inputSchema: {
    type: "object";
    properties: {
      ticket_id: {
        type: "string";
        description: "Jira ticket ID (e.g., 'PROJ-123')";
      };
      output_path?: {
        type: "string";
        description: "Path for generated component (optional, defaults to current directory)";
      };
    };
    required: ["ticket_id"];
  };
  // Returns: Analysis summary + generated component code
}

// Individual analysis tools for flexibility
interface AnalyzeTicketTool {
  name: "analyze_ticket";
  description: "Fetch and analyze a Jira ticket to extract structured requirements, acceptance criteria, and linked design assets.";
  inputSchema: {
    type: "object";
    properties: {
      ticket_id: {
        type: "string";
        description: "Jira ticket ID (e.g., 'PROJ-123')";
      };
    };
    required: ["ticket_id"];
  };
  // Returns: Structured requirements object
}

interface AnalyzeDesignTool {
  name: "analyze_design";
  description: "Analyze a Figma design to extract component structure, identify states (loading/error/empty), and detect accessibility gaps.";
  inputSchema: {
    type: "object";
    properties: {
      figma_url: {
        type: "string";
        description: "Figma file URL or node URL";
      };
    };
    required: ["figma_url"];
  };
  // Returns: Design analysis with component tree, states, tokens, gaps
}

interface GenerateComponentTool {
  name: "generate_component";
  description: "Generate an Angular component from a specification, matching patterns from the current workspace.";
  inputSchema: {
    type: "object";
    properties: {
      name: {
        type: "string";
        description: "Component name (e.g., 'user-card')";
      };
      spec: {
        type: "object";
        description: "Component specification from analysis";
        properties: {
          inputs: { type: "array"; description: "Component @Input() bindings" };
          outputs: { type: "array"; description: "Component @Output() events" };
          states: { type: "array"; description: "UI states to handle" };
          design_tokens: { type: "object"; description: "Design system tokens" };
        };
      };
    };
    required: ["name", "spec"];
  };
  // Returns: Generated files (component.ts, template.html, styles.scss, spec.ts)
}
```

---

## Differentiators (Nice to Have)

Features that would enhance the demo if time permits. Order by impact/effort ratio.

| Tool | Purpose | Complexity | Priority | Notes |
|------|---------|------------|----------|-------|
| `review_code` | Check generated code against workspace patterns | Medium | P1 | High demo impact, shows quality gates |
| `get_workspace_patterns` | Extract coding patterns from current Angular project | Medium | P2 | Improves generation quality |
| `suggest_subtasks` | Generate Jira subtask breakdown from analysis | Low | P3 | Shows actionable output |
| `get_design_gaps` | Detailed missing states report | Low | P3 | Already part of analyze_design |

### Optional Tool Signatures

```typescript
interface ReviewCodeTool {
  name: "review_code";
  description: "Review generated or existing code against workspace patterns and Angular best practices.";
  inputSchema: {
    type: "object";
    properties: {
      code: {
        type: "string";
        description: "Code to review (or file path)";
      };
      check_patterns?: {
        type: "boolean";
        default: true;
        description: "Check against workspace patterns";
      };
      check_accessibility?: {
        type: "boolean";
        default: true;
        description: "Check for accessibility issues";
      };
    };
    required: ["code"];
  };
  // Returns: Review findings with suggestions
}

interface GetWorkspacePatternsTool {
  name: "get_workspace_patterns";
  description: "Analyze the current Angular workspace to extract component patterns, naming conventions, and coding standards.";
  inputSchema: {
    type: "object";
    properties: {
      scope?: {
        type: "string";
        enum: ["components", "services", "all"];
        default: "components";
        description: "What to analyze";
      };
    };
  };
  // Returns: Extracted patterns for generation guidance
}
```

---

## Anti-Features (Skip These)

Features that seem valuable but should be avoided given constraints.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Jira write access | Risk of polluting real projects, auth complexity | Show suggested subtasks as output text, manual copy |
| Full Figma plugin | Time-intensive, separate distribution | Use Figma REST API + existing Figma MCP server |
| Multi-file refactoring | Scope creep, high risk | Generate single component, user integrates |
| Real-time design sync | Complex state management | Point-in-time analysis, user re-runs when needed |
| Custom LLM hosting | Azure OpenAI is mandated | Use Azure OpenAI only |
| Production-ready error handling | Overkill for demo | Happy path focus, basic error messages |

---

## Leverage Existing MCP Ecosystem

**Critical insight:** Don't rebuild what exists. These MCP servers are production-ready:

### Figma MCP Server (Official)

Use for design context extraction. Available tools:
- `get_design_context` - Extracts design context with component structure
- `get_variable_defs` - Returns design tokens (colors, spacing, typography)
- `get_code_connect_map` - Maps Figma nodes to code components
- `get_screenshot` - Captures selection for visual reference
- `get_metadata` - Returns layer structure as XML

**Recommendation:** If team has Figma Dev seat, use official Figma MCP directly. Call it from your orchestration agent rather than reimplementing.

Source: [Figma MCP Tools Documentation](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)

### Atlassian MCP Server (Official)

Use for Jira access. Available capabilities:
- Search issues with JQL
- Get issue details with all fields
- Support for Cloud and Server/Data Center

**Recommendation:** Consider using official Atlassian MCP or community `mcp-atlassian` package. Saves significant development time.

Sources:
- [Atlassian Remote MCP Server](https://github.com/atlassian/atlassian-mcp-server)
- [mcp-atlassian community server](https://github.com/sooperset/mcp-atlassian)

### Angular CLI MCP Server (Official)

Use for Angular scaffolding. Available tools:
- `ng generate` - Scaffold components, services, etc.
- `get_best_practices` - Current Angular coding standards
- `search_documentation` - Query angular.dev

**Recommendation:** Delegate component scaffolding to Angular CLI MCP. Your tool adds value by providing the right parameters based on analysis.

Source: [Angular CLI MCP Server](https://angular.dev/ai/mcp)

### ESLint MCP Server (Official)

Use for code quality checks. Available via `eslint --mcp` flag.

**Recommendation:** Use for the `review_code` tool if time permits.

Source: [ESLint MCP Setup](https://eslint.org/docs/latest/use/mcp)

---

## Architecture Decision: Thin MCP, Fat Agents

Given the existing ecosystem, your MCP server should be **thin**:

```
VS Code Copilot
    |
    v
Your MCP Server (thin)
    |-- accelerate tool
    |-- analyze_ticket tool
    |-- analyze_design tool
    |-- generate_component tool
    |
    v
Python Backend (fat - agent logic here)
    |-- Ticket Analyzer Agent (calls Jira API)
    |-- Design Analyzer Agent (calls Figma API)
    |-- Generator Agent (uses Azure OpenAI)
    |-- Pattern Extractor (reads workspace)
    |
    v
External Services
    |-- Jira Cloud API
    |-- Figma REST API
    |-- Azure OpenAI
```

**Why this architecture:**
1. MCP is just the interface - keep it simple
2. Agent logic in Python is easier to iterate
3. Can test agents independently of MCP
4. Existing MCP servers can be composed later

---

## MVP Feature Set for Hackathon

### Hour 1-2: Core Pipeline

| Component | Owner | Deliverable |
|-----------|-------|-------------|
| MCP Server skeleton | Frontend 1 | 4 tool stubs that call Python backend |
| Jira API client | Frontend 2 | Fetch ticket by ID, parse fields |
| Figma API client | Frontend 2 | Fetch design node, extract structure |
| Agent orchestration | Full-stack | Pipeline: ticket -> analysis -> generation |

### Hour 2-3: Integration

| Component | Owner | Deliverable |
|-----------|-------|-------------|
| Ticket Analyzer Agent | Full-stack | Structured requirements from ticket |
| Design Analyzer Agent | Full-stack | Component structure + gap detection |
| Component Generator | Full-stack | Angular code from spec |
| MCP integration | Frontend 1 | Tools calling Python endpoints |

### Hour 3-4: Demo Polish

| Component | Owner | Deliverable |
|-----------|-------|-------------|
| End-to-end `accelerate` | Full-stack | Single command demo flow |
| Sample data | BA + Designers | Real ticket + Figma design |
| Demo script | BA | Rehearsed walkthrough |

---

## Input/Output Contracts

### analyze_ticket Output

```json
{
  "ticket_id": "PROJ-123",
  "title": "Create user profile card component",
  "type": "story",
  "requirements": {
    "user_stories": [
      "As a user, I want to see my profile information at a glance"
    ],
    "acceptance_criteria": [
      "Shows user avatar, name, and role",
      "Displays last active timestamp",
      "Handles loading and error states"
    ],
    "technical_notes": [
      "Use existing Avatar component",
      "Follow card pattern from design system"
    ]
  },
  "linked_designs": [
    {
      "type": "figma",
      "url": "https://figma.com/file/xxx/yyy?node-id=123",
      "label": "User Profile Card Design"
    }
  ],
  "gaps_identified": [
    "No error state specified in AC",
    "Mobile responsive behavior not defined"
  ]
}
```

### analyze_design Output

```json
{
  "figma_url": "https://figma.com/file/xxx/yyy?node-id=123",
  "component_name": "UserProfileCard",
  "structure": {
    "root": "Card",
    "children": ["Avatar", "UserInfo", "StatusBadge"]
  },
  "states_detected": ["default", "loading"],
  "states_missing": ["error", "empty"],
  "design_tokens": {
    "colors": {"background": "surface-primary", "text": "text-default"},
    "spacing": {"padding": "space-4", "gap": "space-2"},
    "typography": {"name": "heading-sm", "role": "body-md"}
  },
  "accessibility_notes": [
    "Needs aria-label for avatar image",
    "Status badge should have sr-only text"
  ],
  "implementation_hints": [
    "Use flexbox for layout",
    "Avatar is 48x48 with rounded-full"
  ]
}
```

### generate_component Output

```json
{
  "component_name": "UserProfileCardComponent",
  "files": {
    "user-profile-card.component.ts": "// Component class code...",
    "user-profile-card.component.html": "<!-- Template -->...",
    "user-profile-card.component.scss": "// Styles...",
    "user-profile-card.component.spec.ts": "// Tests..."
  },
  "notes": [
    "Added loading and error states not in original design",
    "Used OnPush change detection per workspace patterns",
    "Integrated with existing Avatar component"
  ]
}
```

---

## Sources

**MCP Specification:**
- [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- [MCP Architecture Overview](https://modelcontextprotocol.io/docs/learn/architecture)
- [MCP Tools Concept](https://modelcontextprotocol.io/docs/concepts/tools)

**Figma Integration:**
- [Figma MCP Server Introduction](https://www.figma.com/blog/introducing-figma-mcp-server/)
- [Figma MCP Tools and Prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
- [Figma REST API](https://developers.figma.com/docs/rest-api/)

**Jira Integration:**
- [Atlassian Remote MCP Server](https://github.com/atlassian/atlassian-mcp-server)
- [mcp-atlassian Community Server](https://github.com/sooperset/mcp-atlassian)
- [Jira REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/)

**Angular:**
- [Angular CLI MCP Server](https://angular.dev/ai/mcp)

**Code Quality:**
- [ESLint MCP Server](https://eslint.org/docs/latest/use/mcp)

**AI Coding Assistants (Context):**
- [Cline vs Cursor Comparison](https://cline.bot/blog/best-ai-coding-assistant-2025-complete-guide-to-cline-and-cursor)
- [Coding Agents Comparison](https://artificialanalysis.ai/insights/coding-agents-comparison)
