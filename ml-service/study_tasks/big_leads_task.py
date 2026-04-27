import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("leads_big.csv")

features = [
  "sessions_count",
  "page_views_count",
  "time_on_site_sec",
  "viewed_pricing",
  "downloaded_pdf",
  "requested_budget",
  "company_size",
]

x = df[features]
y = df["deal_won"]


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42) 

print(y_test)

log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)

forest_model = RandomForestClassifier(n_estimators=100, random_state=42)
forest_model.fit(X_train, y_train)

log_predictions = log_model.predict(X_test)
log_probabilities = log_model.predict_proba(X_test)[:, 1]
forest_predictions = forest_model.predict(X_test)
forest_probabilities = forest_model.predict_proba(X_test)[:, 1]

print("\nLogistic Regression predictions:")
print(log_predictions)

print("\nLogistic Regression probabilities:")
print(log_probabilities)

print("\nRandom Forest predictions:")
print(forest_predictions)

print("\nRandom Forest probabilities:")
print(forest_probabilities)

print("\nLogistic Regression coefficients:")
for feature, coef in zip(features, log_model.coef_[0]):
    print(feature, coef)

print("\nRandom Forest feature importances:")
for feature, importance in zip(features, forest_model.feature_importances_):
    print(feature, importance)
