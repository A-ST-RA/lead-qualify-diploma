from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import numpy as np

import pandas as pd

df = pd.read_csv("leads_big.csv")

numeric_features = [
    "sessions_count",
    "page_views_count",
    "time_on_site_sec",
    "requested_budget",
    "company_size",
]

categorical_features = ["source", "industry"]

binary_features = ["viewed_pricing", "downloaded_pdf"]

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

preprocessor = ColumnTransformer([
    ("numeric", numeric_transformer, numeric_features),
    ("categorical", categorical_transformer, categorical_features),
    ("binary", binary_transformer, binary_features),
])

model_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=1000)),
])

X = df[numeric_features + categorical_features + binary_features]
y = df["deal_won"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

model_pipeline.fit(X_train, y_train)

new_lead = pd.DataFrame([{
    "sessions_count": 3,
    "page_views_count": 8,
    "time_on_site_sec": 300,
    "requested_budget": 90000,
    "company_size": 25,
    "source": "telegram_ads",
    "industry": np.nan,
    "viewed_pricing": 1,
    "downloaded_pdf": 0,
}])

print("New lead probability:")
print(model_pipeline.predict_proba(new_lead)[:, 1])

transformed = model_pipeline.named_steps["preprocessor"].transform(new_lead)

print("Transformed new lead:")
print(transformed)
print("Shape:")
print(transformed.shape)

feature_names = model_pipeline.named_steps["preprocessor"].get_feature_names_out()

for name, value in zip(feature_names, transformed[0]):
    print(name, value)
