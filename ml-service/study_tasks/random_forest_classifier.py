import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix


# Загружаем данные
df = pd.read_csv("leads_big.csv")

# Выбираем признаки
features = [
    "sessions_count",
    "page_views_count",
    "time_on_site_sec",
    "viewed_pricing",
    "downloaded_pdf",
    "requested_budget",
    "company_size",
]

X = df[features]
y = df["deal_won"]

# Разделяем данные на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

forest_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
forest_model.fit(X_train, y_train)

forest_predictions = forest_model.predict(X_test)
forest_probabilities = forest_model.predict_proba(X_test)[:, 1]

preds = forest_model.predict(X_test)

print(confusion_matrix(y_test, preds, labels=[0, 1]))

print(classification_report(y_test, preds, zero_division=0))
