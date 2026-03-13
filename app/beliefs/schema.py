from __future__ import annotations
from typing import Literal, Optional, List
from pydantic import BaseModel, Field, conlist, confloat


BeliefKind = Literal["boundary", "preference", "style", "relationship"]


class BeliefUpdate(BaseModel):
    kind: BeliefKind
    key: Optional[str] = None
    value: str
    strength: confloat(ge=0.0, le=1.0) = 0.7
    evidence_span: str = Field(..., description="Must be a substring of the current user_text.")


class ExtractorOutput(BaseModel):
    should_update: bool
    confidence: confloat(ge=0.0, le=1.0)
    beliefs: List[BeliefUpdate] = Field(default_factory=list)
    notes: Optional[str] = None
