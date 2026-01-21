from enum import Enum
from pydantic import BaseModel


class Severity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class FindingCategory(str, Enum):
    MISSING_STATES = "missing_states"
    ACCESSIBILITY = "accessibility"
    DESIGN_SYSTEM = "design_system"
    RESPONSIVENESS = "responsiveness"


class Finding(BaseModel):
    category: FindingCategory
    severity: Severity
    title: str
    description: str
    recommendation: str
    affected_frames: list[str]


class AnalysisResult(BaseModel):
    findings: list[Finding]
    summary: str
    frames_analyzed: int
