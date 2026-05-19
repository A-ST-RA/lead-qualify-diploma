from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from lead_qualify.config import RANDOM_STATE
from lead_qualify.features import (
    BINARY_FEATURES,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
)


def build_preprocessor() -> ColumnTransformer:
    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="other")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    binary_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value=0)),
    ])

    return ColumnTransformer([
        ("numeric", numeric_transformer, NUMERIC_FEATURES),
        ("categorical", categorical_transformer, CATEGORICAL_FEATURES),
        ("binary", binary_transformer, BINARY_FEATURES),
    ])


def build_classifier() -> RandomForestClassifier:
    return RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        min_samples_leaf=2,
        random_state=RANDOM_STATE,
        class_weight="balanced",
    )


def build_model_pipeline() -> Pipeline:
    return Pipeline([
        ("preprocessor", build_preprocessor()),
        ("model", build_classifier()),
    ])
