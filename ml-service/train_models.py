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

# Обучаем модель логистической регрессии
log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)

# forest_model = RandomForestClassifier(
#     n_estimators=100,
#     random_state=42
# )
# forest_model.fit(X_train, y_train)

log_predictions = log_model.predict(X_test)
log_probabilities = log_model.predict_proba(X_test)[:, 1]

# forest_predictions = forest_model.predict(X_test)
# forest_probabilities = forest_model.predict_proba(X_test)[:, 1]

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

new_predictions = log_model.predict(new_leads)
new_probabilities = log_model.predict_proba(new_leads)[:, 1]

print("\nNew leads:")
print(new_leads)

print("\nNew lead predictions:")
print(new_predictions)

print("\nNew lead probabilities:")
print(new_probabilities)

budget_test_leads = pd.DataFrame([
    {
        "sessions_count": 3,
        "page_views_count": 8,
        "time_on_site_sec": 350,
        "viewed_pricing": 1,
        "downloaded_pdf": 0,
        "requested_budget": 10000,
        "company_size": 25,
    },
    {
        "sessions_count": 3,
        "page_views_count": 8,
        "time_on_site_sec": 350,
        "viewed_pricing": 1,
        "downloaded_pdf": 0,
        "requested_budget": 50000,
        "company_size": 25,
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
        "sessions_count": 3,
        "page_views_count": 8,
        "time_on_site_sec": 350,
        "viewed_pricing": 1,
        "downloaded_pdf": 0,
        "requested_budget": 150000,
        "company_size": 25,
    },
])

budget_probabilities = log_model.predict_proba(budget_test_leads)[:, 1]

print("\nBudget sensitivity test:")
for budget, probability in zip(budget_test_leads["requested_budget"], budget_probabilities):
    print("budget:", budget, "probability:", probability)

