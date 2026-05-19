from pathlib import Path

ML_SERVICE_ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = ML_SERVICE_ROOT / "artifacts"
DEFAULT_MODEL_PATH = ARTIFACTS_DIR / "model.joblib"
DEFAULT_METRICS_PATH = ARTIFACTS_DIR / "metrics.json"
DEFAULT_DATA_PATH = ML_SERVICE_ROOT / "study_tasks" / "leads_big.csv"

RANDOM_STATE = 42
TEST_SIZE = 0.25
PREDICTION_THRESHOLD = 0.5

TARGET_COLUMN = "deal_won"
