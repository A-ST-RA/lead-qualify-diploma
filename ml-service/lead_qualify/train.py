import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

import sklearn

from lead_qualify.config import (
    DEFAULT_DATA_PATH,
    DEFAULT_METRICS_PATH,
    DEFAULT_MODEL_PATH,
    RANDOM_STATE,
    TARGET_COLUMN,
    TEST_SIZE,
)
from lead_qualify.features import FEATURE_COLUMNS
from lead_qualify.pipeline import build_model_pipeline


def load_dataset(data_path: Path) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(data_path)

    missing_columns = set(FEATURE_COLUMNS + [TARGET_COLUMN]) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in dataset: {sorted(missing_columns)}")

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    return X, y


def evaluate_model(pipeline, X_test, y_test) -> dict:
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1": float(f1_score(y_test, y_pred, zero_division=0)),
    }

    if len(set(y_test)) > 1:
        metrics["roc_auc"] = float(roc_auc_score(y_test, y_prob))
    else:
        metrics["roc_auc"] = None

    return metrics


def train(
    data_path: Path,
    model_path: Path,
    metrics_path: Path,
) -> dict:
    X, y = load_dataset(data_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    eval_pipeline = build_model_pipeline()
    eval_pipeline.fit(X_train, y_train)
    holdout_metrics = evaluate_model(eval_pipeline, X_test, y_test)

    final_pipeline = build_model_pipeline()
    final_pipeline.fit(X, y)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(final_pipeline, model_path)

    metadata = {
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "data_path": str(data_path),
        "n_samples": len(X),
        "sklearn_version": sklearn.__version__,
        "holdout_metrics": holdout_metrics,
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
    }

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Train lead qualification model")
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to training CSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help="Path to save trained pipeline",
    )
    parser.add_argument(
        "--metrics",
        type=Path,
        default=DEFAULT_METRICS_PATH,
        help="Path to save training metrics JSON",
    )
    args = parser.parse_args()

    metadata = train(args.data, args.output, args.metrics)

    print(f"Model saved to {args.output}")
    print(f"Metrics saved to {args.metrics}")
    print("Hold-out metrics:")
    for name, value in metadata["holdout_metrics"].items():
        print(f"  {name}: {value}")


if __name__ == "__main__":
    main()
