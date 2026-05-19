from typing import Optional

from pydantic import BaseModel, Field

from lead_qualify.config import PREDICTION_THRESHOLD


class LeadFeaturesIn(BaseModel):
    sessions_count: int = Field(..., ge=0)
    page_views_count: int = Field(..., ge=0)
    time_on_site_sec: int = Field(..., ge=0)
    requested_budget: float = Field(..., ge=0)
    company_size: int = Field(..., ge=0)
    source: str
    industry: Optional[str] = None
    viewed_pricing: int = Field(..., ge=0, le=1)
    downloaded_pdf: int = Field(..., ge=0, le=1)

    def to_feature_dict(self) -> dict:
        return self.model_dump()


class PredictResponse(BaseModel):
    probability: float = Field(..., ge=0, le=1)
    predicted_class: int = Field(..., ge=0, le=1)
    threshold: float = PREDICTION_THRESHOLD


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


class ModelInfoResponse(BaseModel):
    model_loaded: bool
    feature_columns: list[str]
    metrics: Optional[dict] = None
