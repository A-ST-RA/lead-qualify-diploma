import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# Загружаем данные
df = pd.read_csv("leads.csv")

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

print("\nRandom Forest predictions:")
print(forest_predictions)

print("\nRandom Forest probabilities:")
print(forest_probabilities)

new_leads = pd.DataFrame([
    {
        "sessions_count": 1,
        "page_views_count": 2,
        "time_on_site_sec": 45,
        "viewed_pricing": 0,
        "downloaded_pdf": 0,
        "requested_budget": 15000,
        "company_size": 4,
    },
    {
        "sessions_count": 3,
        "page_views_count": 8,
        "time_on_site_sec": 350,
        "viewed_pricing": 1,
        "downloaded_pdf": 0,
        "requested_budget": 90000,
        "company_size": 25,
    },
    {
        "sessions_count": 5,
        "page_views_count": 15,
        "time_on_site_sec": 800,
        "viewed_pricing": 1,
        "downloaded_pdf": 1,
        "requested_budget": 250000,
        "company_size": 120,
    },
])

forest_new_predictions = forest_model.predict(new_leads)
forest_new_probabilities = forest_model.predict_proba(new_leads)[:, 1]

print("\nRandom Forest new lead predictions:")
print(forest_new_predictions)

print("\nRandom Forest new lead probabilities:")
print(forest_new_probabilities)