from fastapi import APIRouter, Request, HTTPException
from openai import APIError, RateLimitError
from ..models.request import DesignDataRequest
from ..models.response import AnalysisResult
from ..services.analyzer import analyze_design

router = APIRouter(prefix="/review", tags=["review"])


@router.post("/analyze", response_model=AnalysisResult)
async def analyze(request: Request, data: DesignDataRequest) -> AnalysisResult:
    """
    Analyze design data for completeness issues.

    Checks for:
    - Missing UI states (loading, error, empty, disabled, hover, focus, pressed)
    - Accessibility gaps (contrast, labels, focus indicators, touch targets)
    - Design system violations (spacing, colors, typography)
    - Responsiveness gaps (missing breakpoints)

    Returns structured findings with severity and recommendations.
    """
    client = request.app.state.openai_client
    settings = request.app.state.settings

    try:
        result = await analyze_design(
            client=client,
            deployment=settings.azure_openai_deployment,
            design_data=data,
        )
        return result
    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="Azure OpenAI rate limit exceeded. Please try again shortly.",
        )
    except APIError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Azure OpenAI error: {str(e)}",
        )
