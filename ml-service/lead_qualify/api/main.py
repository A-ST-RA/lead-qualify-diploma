import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from lead_qualify.config import (
    DEFAULT_METRICS_PATH,
    DEFAULT_MODEL_PATH,
    PREDICTION_THRESHOLD,
)
from lead_qualify.features import FEATURE_COLUMNS
from lead_qualify.schemas import (
    HealthResponse,
    LeadFeaturesIn,
    ModelInfoResponse,
    PredictResponse,
)

MODEL_PATH = Path(DEFAULT_MODEL_PATH)
METRICS_PATH = Path(DEFAULT_METRICS_PATH)

_model: Optional[object] = None
_metrics: Optional[dict] = None


def load_model() -> None:
    global _model, _metrics

    if MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    else:
        _model = None

    if METRICS_PATH.exists():
        with METRICS_PATH.open(encoding="utf-8") as f:
            _metrics = json.load(f)
    else:
        _metrics = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    yield


app = FastAPI(
    title="Lead Qualify ML Service",
    description="Predicts probability that a lead will win (deal_won=1)",
    version="0.1.0",
    lifespan=lifespan,
)


def require_model():
    if _model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Train the model first: python -m lead_qualify.train",
        )
    return _model


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        model_loaded=_model is not None,
    )


@app.get("/model/info", response_model=ModelInfoResponse)
def model_info():
    return ModelInfoResponse(
        model_loaded=_model is not None,
        feature_columns=FEATURE_COLUMNS,
        metrics=_metrics,
    )


@app.post("/predict", response_model=PredictResponse)
def predict(lead: LeadFeaturesIn):
    model = require_model()

    row = pd.DataFrame([lead.to_feature_dict()])
    probability = float(model.predict_proba(row)[0, 1])
    predicted_class = int(probability >= PREDICTION_THRESHOLD)

    return PredictResponse(
        probability=probability,
        predicted_class=predicted_class,
        threshold=PREDICTION_THRESHOLD,
    )
