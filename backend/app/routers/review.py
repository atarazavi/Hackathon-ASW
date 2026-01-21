from fastapi import APIRouter, Request, HTTPException
from ..models.request import DesignDataRequest
from ..models.response import AnalysisResult, Finding, Severity, FindingCategory

router = APIRouter(prefix="/review", tags=["review"])


@router.post("/analyze", response_model=AnalysisResult)
async def analyze(request: Request, data: DesignDataRequest) -> AnalysisResult:
    """
    Analyze design data for completeness issues.

    Stub implementation - returns empty findings.
    Real analysis added in Plan 02.
    """
    # Access client (will be used in Plan 02)
    client = request.app.state.openai_client
    settings = request.app.state.settings

    # Return stub response for now
    return AnalysisResult(
        findings=[],
        summary="Analysis pending - stub response",
        frames_analyzed=len(data.frames),
    )
