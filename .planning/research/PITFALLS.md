# Domain Pitfalls: MCP Hackathon Build

**Domain:** MCP Server + Multi-Agent Hackathon (3-4 hours, 6 people)
**Researched:** 2026-01-21
**Confidence:** HIGH (multiple authoritative sources)

---

## Critical Pitfalls (Will Kill Your Demo)

### 1. Stdout Pollution Breaks MCP Completely

**What goes wrong:** MCP's stdio transport uses stdout exclusively for JSON-RPC messages. ANY print statement, debug output, or logging to stdout corrupts the entire message stream. Your MCP server appears to "not work" with no clear error.

**Warning signs:**
- MCP client shows "connection failed" or hangs
- Tools don't appear in the tools list
- Server seems to start but client never connects

**Prevention:**
```python
# WRONG - breaks MCP
print("Debug info")
logging.basicConfig()  # defaults to stdout

# RIGHT - all output to stderr
import sys
print("Debug info", file=sys.stderr)
logging.basicConfig(stream=sys.stderr)
```

**Quick workaround if hit:** Search your entire codebase for `print(` and redirect all to stderr. Set `FASTMCP_LOG_LEVEL=DEBUG` in environment to see what's happening.

**Source:** [MCP Debugging Guide](https://modelcontextprotocol.io/legacy/tools/debugging), [Nearform MCP Tips](https://nearform.com/digital-community/implementing-model-context-protocol-mcp-tips-tricks-and-pitfalls/)

---

### 2. Figma API Rate Limits Are Brutal (6 requests/month on Starter)

**What goes wrong:** Figma enforces strict rate limits that vary by plan and seat type. On Starter plans, you get only 6 API requests per month to files outside your project. After hitting the limit, you get a 429 with "Retry-After: 4 days" - not recoverable in a hackathon.

**Warning signs:**
- HTTP 429 Too Many Requests
- Retry-After header showing days, not seconds
- Works for first few requests, then stops

**Prevention:**
- Use a Full seat on a paid Figma plan for the file owner
- Cache ALL Figma responses locally immediately
- Test against your own project files (no rate limit for files you own)
- Have a hardcoded fallback design JSON for demo

**Quick workaround if hit:**
1. Switch to a different Figma account with a Full seat
2. Use pre-cached JSON from an earlier successful request
3. Create a mock Figma response for demo purposes

**Source:** [Figma Rate Limits](https://help.figma.com/hc/en-us/articles/34963238552855-What-if-I-m-rate-limited), [Figma Forum Discussion](https://forum.figma.com/report-a-problem-6/old-limit-on-rest-api-requests-after-purchasing-the-pro-subscription-47661)

---

### 3. Jira Authentication Has Multiple Traps

**What goes wrong:** Jira authentication fails silently or with confusing 401 errors. Common causes: using SSO credentials (never works), using OAuth scoped tokens with REST API (wrong endpoint), CAPTCHA triggered after failed attempts, or deprecated API endpoints.

**Warning signs:**
- HTTP 401 Unauthorized despite correct-looking credentials
- "Authentication required" even with API token
- Works in browser, fails in code

**Prevention:**
- Use API tokens (not SSO passwords) from https://id.atlassian.com/manage-profile/security/api-tokens
- Use correct Cloud endpoint format: `https://your-domain.atlassian.net/rest/api/3/`
- Test authentication FIRST before building anything else
- Avoid failed login attempts (triggers CAPTCHA)

**Quick workaround if hit:**
1. Generate a fresh API token
2. If CAPTCHA triggered: log in to Jira in browser, complete CAPTCHA, then retry API
3. For OAuth tokens, use the Cloud ID URL format: `https://api.atlassian.com/ex/jira/{cloudId}/rest/api/3/`

**Source:** [Jira API Authentication Guide](https://www.getknit.dev/blog/deep-dive-developer-guide-to-building-a-jira-api-integration), [Atlassian Community](https://community.atlassian.com/forums/Jira-questions/Jira-API-fails-to-authenticate/qaq-p/3028744)

---

### 4. Azure OpenAI 429 Errors During Demo

**What goes wrong:** Azure OpenAI rate limits are per-minute with burst protection. During a demo, rapid requests trigger 429 "NoCapacity" errors with retry delays of 30-60+ seconds. Demo grinds to a halt.

**Warning signs:**
- HTTP 429 with "Too Many Requests"
- Responses getting slower before failing completely
- Works fine in testing, fails during high-pressure demo

**Prevention:**
- Request quota increase BEFORE the hackathon (takes time)
- Implement exponential backoff with jitter
- Use streaming responses (starts returning in 5-6 seconds vs timeout)
- Cache LLM responses for demo-specific inputs
- Have pre-generated outputs ready for demo fallback

**Quick workaround if hit:**
1. Wait the Retry-After seconds (usually 30-60s)
2. Switch to pre-cached responses for demo
3. Have a backup deployment in a different Azure region

**Source:** [Azure OpenAI Rate Limits](https://learn.microsoft.com/en-us/answers/questions/1693832/azure-openai-error-429-request-below-rate-limit), [Azure OpenAI Quotas](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/quotas-limits)

---

### 5. VS Code MCP Configuration Silent Failures

**What goes wrong:** VS Code MCP configuration has subtle requirements. Wrong naming, missing uvx installation, or VS Code version bugs cause servers to silently not load. No error, tools just don't appear.

**Warning signs:**
- MCP tools don't appear in Chat view
- Green/yellow/red indicator shows red or nothing
- Works in Inspector, fails in VS Code

**Prevention:**
- Use exact configuration naming (not `mcp-servers` or `mcpservers`)
- Install uvx: `pipx install uv` or `brew install uv`
- Test with MCP Inspector BEFORE VS Code integration
- Use absolute paths in configuration
- Fully quit VS Code (not just reload) after config changes

**Quick workaround if hit:**
1. Check VS Code Output panel: select "MCP Server Extension" from dropdown
2. Run `mcp dev your_server.py` to test independently
3. Restart VS Code completely (not just reload window)
4. Fall back to Claude Desktop or Inspector for demo

**Source:** [VS Code MCP Docs](https://code.visualstudio.com/docs/copilot/customization/mcp-servers), [VS Code MCP Issues](https://github.com/microsoft/vscode/issues/281538)

---

## Moderate Pitfalls (Will Waste Hours)

### 6. Too Many Tools Degrades LLM Performance

**What goes wrong:** LLM reliability negatively correlates with instruction context size. Adding many tools with long descriptions causes inference slowdown, wrong tool calls, and potential timeouts.

**Warning signs:**
- LLM picks wrong tools
- Responses getting slower
- Context window errors

**Prevention:**
- Keep to 5-8 focused tools maximum
- Use short, clear tool descriptions (1-2 sentences)
- Remove tools not needed for demo flow

**Quick workaround:** Temporarily disable non-essential tools for demo.

**Source:** [Merge.dev MCP Challenges](https://www.merge.dev/blog/mcp-challenges), [Everything Wrong with MCP](https://blog.sshh.io/p/everything-wrong-with-mcp)

---

### 7. Git Conflicts from Parallel Agent Work

**What goes wrong:** Multiple developers with coding agents working on the same branch create massive merge conflicts. Resolving conflicts takes more time than the original work.

**Warning signs:**
- Multiple people editing same files
- Long time between pulls
- "CONFLICT" appearing in git merge

**Prevention:**
- One developer per branch/feature
- Use Git worktrees for parallel agent work
- Modularize aggressively: separate concerns into different files
- Pull and merge frequently (every 30 minutes minimum)
- Designate one "integration lead" for the main branch

**Quick workaround:** If deep in conflicts, one person takes lead, others pause. Alternatively, pick one version and re-apply changes manually.

**Source:** [Git Worktrees for AI Development](https://www.tamirdresher.com/blog/2025/10/20/scaling-your-ai-development-team-with-git-worktrees), [Parallel AI Development](https://medium.com/@ooi_yee_fei/parallel-ai-development-with-git-worktrees-f2524afc3e33)

---

### 8. Working Directory Undefined in MCP

**What goes wrong:** When MCP server is launched via VS Code or Claude Desktop, the working directory may be undefined (like `/` on macOS). Relative paths fail silently.

**Warning signs:**
- File operations fail with "not found"
- Server works in terminal, fails in client
- Inconsistent behavior between environments

**Prevention:**
- Use ABSOLUTE paths everywhere in MCP server code
- Use absolute paths in configuration files and .env
- Pass base directory as argument if needed

**Quick workaround:** Add this at start of server:
```python
import os
os.chdir("/path/to/your/project")  # Set explicit working directory
```

**Source:** [MCP Debugging Tips](https://www.mcpevals.io/blog/debugging-mcp-servers-tips-and-best-practices)

---

### 9. Type Hints Required for Tool Serialization

**What goes wrong:** FastMCP requires type hints on all tool parameters and return types. Classes without hints can't be serialized for schema generation. Tools silently fail or produce cryptic errors.

**Warning signs:**
- "Cannot serialize" errors
- Tools appear but fail when called
- Schema generation errors

**Prevention:**
```python
# WRONG
def get_component(ticket_id):
    return component

# RIGHT
def get_component(ticket_id: str) -> dict:
    return {"component": component}
```

**Quick workaround:** Add `-> dict` return type and wrap all returns in a dictionary.

**Source:** [FastMCP Tutorial](https://www.firecrawl.dev/blog/fastmcp-tutorial-building-mcp-servers-python)

---

### 10. List Returns Break Some Clients

**What goes wrong:** If your MCP tool returns a top-level list, some clients fail to handle it correctly. Errors may be cryptic or the response appears empty.

**Warning signs:**
- Empty responses when data exists
- Client parsing errors
- Works in Inspector, fails in VS Code

**Prevention:**
```python
# WRONG
return [item1, item2, item3]

# RIGHT
return {"items": [item1, item2, item3]}
```

**Quick workaround:** Wrap any list return in a dictionary.

**Source:** [FastMCP Best Practices](https://pypi.org/project/fastmcp/1.0/)

---

## Minor Pitfalls (Will Cause Annoyance)

### 11. Figma Scope Changes (November 2025)

**What goes wrong:** Figma deprecated `files:read` scope. Apps must use new granular scopes like `file_content:read` and `file_metadata:read`.

**Prevention:** Use new granular scopes when setting up OAuth. For hackathon, personal access token may be simpler.

**Source:** [Figma API Updates](https://developers.figma.com/docs/updates-to-figmas-developer-platform/)

---

### 12. Jira Search API Changed (October 2025)

**What goes wrong:** Old Jira search endpoint was replaced. New endpoint uses `nextpagetoken` for pagination instead of `startat`.

**Prevention:** Use current API endpoint: `/rest/api/3/search/jql` with new pagination.

**Source:** [Atlassian Community](https://community.atlassian.com/forums/Jira-questions/Changes-to-API-token-functionality-around-Oct-1-2025/qaq-p/3124394)

---

### 13. Closing Window Doesn't Restart MCP

**What goes wrong:** Closing Claude Desktop or VS Code window doesn't kill the MCP server process. Config changes don't take effect, old code keeps running.

**Prevention:** Fully quit the application (Cmd+Q on Mac) before testing config changes.

**Source:** [MCP Debugging Guide](https://modelcontextprotocol.io/legacy/tools/debugging)

---

## Demo-Day Specific Risks

### 14. Live Demo Fails, No Backup

**What goes wrong:** Network issues, API outages, or unexpected errors during demo. Judges see failure instead of product.

**Warning signs:** You're still coding features 10 minutes before demo.

**Prevention:**
- Record a screen capture of working demo as backup
- Have pre-populated data that's guaranteed to work
- Test the EXACT demo flow 3+ times before presenting
- Prepare "click-enabled UI mockups" as last resort

**Quick workaround:** "Let me show you a recording of this working" + switch to video.

**Source:** [Devpost Demo Tips](https://info.devpost.com/blog/how-to-present-a-successful-hackathon-demo), [TechCrunch Demo Guide](https://techcrunch.com/2014/09/01/how-to-crush-your-hackathon-demo/)

---

### 15. Demo Takes Too Long

**What goes wrong:** Showing login flows, waiting for API responses, explaining implementation details. Judges lose interest or you run out of time.

**Prevention:**
- Skip authentication flows - start already logged in
- Pre-populate any needed data
- Have text copied to clipboard instead of typing
- Practice to hit time limit with 30s buffer
- Focus on the "wow" moment: ticket ID -> generated component

**Quick workaround:** Skip straight to the result and explain backwards.

**Source:** [Circles.Life Hackathon Pitch](https://medium.com/circleslife/creating-a-5-minute-kickass-hackathon-pitch-17cdcb42c3bc)

---

### 16. Wrong Person Presents

**What goes wrong:** Technical lead presents but isn't a strong communicator. Great project, poor pitch. Judges don't understand the value.

**Prevention:**
- Best communicator presents (not necessarily the tech lead)
- One person presents, others answer questions
- Prepare backup slides for anticipated questions

**Source:** [Hack Upstate Demo Tips](https://medium.com/upstate-interactive/8-tips-to-a-successful-hackathon-demo-and-presentation-4d1ae83415ad)

---

## Team Coordination Risks

### 17. Integration Never Happens

**What goes wrong:** Team splits up to build components in parallel. Components never get integrated. Demo shows 3 disconnected pieces.

**Warning signs:**
- "I'll work on X, you work on Y, we'll connect later"
- No integration checkpoint scheduled
- Different assumptions about interfaces

**Prevention:**
- Define interfaces/contracts FIRST (30 min at start)
- Schedule integration checkpoint at 2-hour mark (50% through)
- Have one person as "integration lead" who doesn't build features
- Build the happy path end-to-end first, then add features

**Source:** [Hackathon Guide](https://hackathon.guide/)

---

### 18. Scope Creep Destroys MVP

**What goes wrong:** Team adds features instead of finishing core flow. Demo shows half-built everything instead of complete something.

**Warning signs:**
- "It would be cool if we also..."
- Core feature not working at 50% time
- Multiple in-progress features, zero complete

**Prevention:**
- Define MVP in first 15 minutes: ticket ID -> generated component
- Anything else is "nice to have" and written on a "do not touch until MVP works" list
- Ruthlessly cut scope at 50% checkpoint

**Source:** [Holistic AI Hackathon Learnings](https://www.holisticai.com/blog/what-we-learned-from-the-great-agent-hack-2025)

---

## Phase-Specific Warnings

| Phase | Likely Pitfall | Mitigation |
|-------|---------------|------------|
| API Setup (first 30 min) | Auth failures block everything | Test auth immediately, have backup credentials |
| MCP Server Build | Stdout pollution, no debugging | Use MCP Inspector, log to stderr |
| Jira Integration | Wrong API version, auth issues | Use API token, verify endpoint format |
| Figma Integration | Rate limits destroy testing | Cache responses, use files you own |
| Azure OpenAI | Rate limits during integration | Implement retry logic, cache responses |
| VS Code Integration | Silent config failures | Test in Inspector first |
| Demo Prep (last 30 min) | No backup, no practice | Record video, practice 3x |

---

## Time Budget Recommendation

For 3-4 hour hackathon with 6 people:

| Time | Activity | Anti-Pitfall |
|------|----------|--------------|
| 0:00-0:15 | Define MVP + interfaces | Prevents scope creep + integration failure |
| 0:15-0:30 | Test ALL API auth | Catches auth failures early |
| 0:30-2:00 | Build in parallel | Use git worktrees, one person per branch |
| 2:00-2:30 | Integration checkpoint | Force integration, cut scope if needed |
| 2:30-3:00 | Complete happy path | One working flow beats many broken ones |
| 3:00-3:30 | Demo prep + practice | Record backup video |
| 3:30-4:00 | Demo | Best communicator presents |

---

## Quick Reference: The "DO NOT" List

1. DO NOT print to stdout in MCP server code
2. DO NOT use relative paths in MCP config
3. DO NOT test Figma API on files you don't own
4. DO NOT use SSO credentials for Jira API
5. DO NOT add features before MVP works
6. DO NOT integrate at the end (integrate at 50%)
7. DO NOT demo without a backup video
8. DO NOT have the quiet dev present

---

## Sources

**MCP/Protocol:**
- [Nearform MCP Tips](https://nearform.com/digital-community/implementing-model-context-protocol-mcp-tips-tricks-and-pitfalls/)
- [MCP Challenges - Merge.dev](https://www.merge.dev/blog/mcp-challenges)
- [Everything Wrong with MCP](https://blog.sshh.io/p/everything-wrong-with-mcp)
- [MCP Debugging Guide](https://modelcontextprotocol.io/legacy/tools/debugging)
- [MCP Evaluation Best Practices](https://www.mcpevals.io/blog/debugging-mcp-servers-tips-and-best-practices)

**APIs:**
- [Figma Rate Limits](https://help.figma.com/hc/en-us/articles/34963238552855-What-if-I-m-rate-limited)
- [Figma Developer Updates](https://developers.figma.com/docs/updates-to-figmas-developer-platform/)
- [Jira API Deep Dive](https://www.getknit.dev/blog/deep-dive-developer-guide-to-building-a-jira-api-integration)
- [Azure OpenAI Rate Limits](https://learn.microsoft.com/en-us/answers/questions/1693832/azure-openai-error-429-request-below-rate-limit)

**Hackathon:**
- [Why AI Agent Pilots Fail](https://composio.dev/blog/why-ai-agent-pilots-fail-2026-integration-roadmap)
- [Multi-Agent Arena Learnings](https://towardsdatascience.com/multi-agent-arena-london-great-agent-hack-2025/)
- [Hackathon Demo Tips](https://info.devpost.com/blog/how-to-present-a-successful-hackathon-demo)
- [Git Worktrees for AI Dev](https://www.tamirdresher.com/blog/2025/10/20/scaling-your-ai-development-team-with-git-worktrees)

**FastMCP:**
- [FastMCP Tutorial](https://www.firecrawl.dev/blog/fastmcp-tutorial-building-mcp-servers-python)
- [FastMCP PyPI](https://pypi.org/project/fastmcp/1.0/)

**VS Code:**
- [VS Code MCP Docs](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [VS Code MCP Dev Guide](https://code.visualstudio.com/api/extension-guides/ai/mcp)
