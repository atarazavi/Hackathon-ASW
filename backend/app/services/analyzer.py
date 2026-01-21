from pathlib import Path
from openai import AsyncAzureOpenAI
from ..models.request import DesignDataRequest
from ..models.response import AnalysisResult

GUIDELINES_PATH = Path(__file__).parent.parent.parent / "guidelines" / "GUIDELINES.md"

SYSTEM_PROMPT = """You are a design review expert. Analyze the provided Figma design data and identify issues in four categories:

1. MISSING_STATES: Check for missing UI states. Interactive components should have:
   - loading: State during async operations
   - error: State when operations fail
   - empty: State when no data is available
   - disabled: State when interaction is not available
   - hover: Mouse over state (desktop)
   - focus: Keyboard focus state (accessibility)
   - pressed: State during interaction

2. ACCESSIBILITY: Check for accessibility gaps:
   - contrast ratios: Text should have 4.5:1 ratio (3:1 for large text)
   - labels: All interactive elements need accessible labels
   - focus indicators: Focus state must be visually distinct
   - touch targets: Minimum 44x44px for touch interactions

3. DESIGN_SYSTEM: Check for design system violations:
   - spacing consistency: Use 4px grid (4, 8, 16, 24, 32px)
   - color token usage: Use semantic tokens, not hardcoded values
   - typography scale: Consistent font sizes and weights

4. RESPONSIVENESS: Check for responsiveness gaps when frames suggest responsive design:
   - missing breakpoints: 320 mobile, 768 tablet, 1024 desktop, 1440 wide
   - component adaptation: Elements should respond to width changes
   - touch target scaling: Larger targets on mobile

Severity levels:
- critical: Blocks users or causes accessibility failures (e.g., cannot click button, text unreadable)
- warning: Degrades user experience (e.g., missing loading state, inconsistent spacing)
- info: Nice to fix, polish items (e.g., minor spacing inconsistency)

For each finding:
- Provide a clear, specific title
- Describe exactly what's wrong
- Give an actionable recommendation
- List the affected frame names

Use the guidelines document for reference on expected standards.

Respond with structured findings, a brief summary, and the count of frames analyzed."""


async def analyze_design(
    client: AsyncAzureOpenAI,
    deployment: str,
    design_data: DesignDataRequest,
) -> AnalysisResult:
    """
    Analyze design data using Azure OpenAI structured outputs.

    Args:
        client: AsyncAzureOpenAI client instance
        deployment: Azure OpenAI deployment name
        design_data: Design data request containing frames to analyze

    Returns:
        AnalysisResult with categorized findings, summary, and frame count
    """
    # Load guidelines from file
    try:
        guidelines = GUIDELINES_PATH.read_text()
    except FileNotFoundError:
        guidelines = ""

    # Override with request guidelines if provided
    if design_data.guidelines:
        guidelines = design_data.guidelines

    # Build user prompt with guidelines and design data
    user_prompt = f"""## Design Guidelines
{guidelines}

## Design Data to Analyze
{design_data.model_dump_json(indent=2)}

Analyze this design data and return structured findings."""

    completion = await client.beta.chat.completions.parse(
        model=deployment,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format=AnalysisResult,
        temperature=0.2,
    )

    return completion.choices[0].message.parsed
