import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

df = pd.read_csv("study_tasks/indictaor_task/indicator_task_solve.csv")

numeric_features = [
  "requested_budget",
]

numeric_transformer = Pipeline([
  ("imputer", SimpleImputer(strategy="median", add_indicator=True)),
])

numeric_transformer.fit(df[numeric_features])

transformed = numeric_transformer.transform(df[numeric_features])
print(transformed)